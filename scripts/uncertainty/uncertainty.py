
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import umap
# import torch
import os
from datetime import datetime
import json

###############################################
# 1. Compute the Jaccard similarity matrix
###############################################
def compute_jaccard_matrix(answers):
    """
    Input:
        answers: a list of string answers from an LLM
    Output:
        A square matrix (Jaccard similarity), where
        entry [i,j] indicates the Jaccard score between
        answer i and answer j.
    """
    n = len(answers)
    sets = [set(ans.lower().split()) for ans in answers]
    W = np.eye(n, dtype=np.float32)
    for i in range(n):
        for j in range(i + 1, n):
            union_size = max(len(sets[i].union(sets[j])), 1)
            inter_size = len(sets[i].intersection(sets[j]))
            sim = inter_size / union_size
            W[i, j] = W[j, i] = sim
    return W

###############################################
# 2. Generate the affinity matrix
###############################################
def get_affinity_mat(logits, mode='jaccard', temp=None, symmetric=True):
    """
    Generates an affinity matrix in one of two modes:

      - mode='jaccard':
            Interprets the 'logits' input as an already computed
            Jaccard similarity matrix. Converts it to a NumPy array,
            sets the diagonal to 1, and returns.

      - mode='agreement_w':
            'logits' is assumed to be a (N, N, C) tensor.
            Applies softmax over the last dimension (with temperature),
            extracts probability for category index 2, optionally symmetrizes it,
            sets the diagonal to 1, and returns.
    """
    if mode.lower() == 'jaccard':
        W = np.array(logits).copy()
        np.fill_diagonal(W, 1)
        return W.astype(np.float32)
    
    elif mode.lower() == 'agreement_w':
        if temp is None:
            raise ValueError("agreement_w mode requires a temperature.")
        # logits shape: (N, N, C)
        # 使用numpy实现softmax
        def softmax(x, axis=-1):
            exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
            return exp_x / np.sum(exp_x, axis=axis, keepdims=True)
        
        W = softmax(logits / temp, axis=-1)[:, :, 2]  # Probability of category 2
        if symmetric:
            W = (W + W.T) / 2
        np.fill_diagonal(W, 1)
        return W.astype(np.float32)
    
    else:
        raise ValueError("Only supports 'jaccard' or 'agreement_w' modes.")

###############################################
# 3. Spectral clustering-related functions
###############################################
def get_L_mat(W, symmetric=True):
    """
    Computes the normalized Laplacian matrix
        L = D^{-1/2} * (D - W) * D^{-1/2}
    where D is the degree matrix (diag of row-sum).
    """
    D = np.diag(np.sum(W, axis=1))
    if symmetric:
        inv_sqrt_D = np.diag(1 / (np.sqrt(np.diag(D)) + 1e-8))
        L = inv_sqrt_D @ (D - W) @ inv_sqrt_D
        return L.copy()
    else:
        raise NotImplementedError("Non-symmetric normalization is not implemented.")

def get_eig(L, thres=None, eps=None):
    """
    Computes the eigenvalues and eigenvectors of L.
    If 'thres' is provided, only keeps eigenvalues < thres.
    If 'eps' is provided, applies a small perturbation to L:
        L = (1 - eps) * L + eps * I
    """
    if eps is not None:
        L = (1 - eps) * L + eps * np.eye(L.shape[0])
    eigvals, eigvecs = np.linalg.eigh(L)
    if thres is not None:
        mask = eigvals < thres
        eigvals = eigvals[mask]
        eigvecs = eigvecs[:, mask]
    return eigvals, eigvecs

def spectral_projection(W, eigv_threshold):
    """
    Computes the normalized Laplacian of W, then obtains
    the eigenvectors with eigenvalues < eigv_threshold.
    """
    L = get_L_mat(W, symmetric=True)
    _, eigvecs = get_eig(L, thres=eigv_threshold)
    return eigvecs

def get_eccentricity(W, eigv_threshold):
    """
    Computes the eccentricity as follows:
      1) Projects onto eigenvectors (with L's eigenvalues < eigv_threshold),
      2) For each node (row), compute its distance to the mean vector,
      3) Return the overall L2 norm of those distances (overall_ecc)
         and the array of individual distances ds.
    """
    proj = spectral_projection(W, eigv_threshold)
    ds = np.linalg.norm(proj - proj.mean(axis=0)[None, :], ord=2, axis=1)
    overall_ecc = np.linalg.norm(ds, ord=2)
    return overall_ecc, ds

def get_degreeuq(W):
    """
    Computes the 'Degree Uncertainty' for each node:
        ret[i] = sum_j(1 - W[i,j]),
    and returns the mean across all nodes and the per-node array.
    """
    ret = np.sum(1 - W, axis=1)
    return ret.mean(), ret

def get_eigv_metric(eigvals, threshold=0.9):
    """
    Calculate eigenvalue-based uncertainty metric
    Small eigenvalues indicate stronger clustering structure, so we focus on eigenvalues below threshold
    Returns:
        - Eigenvalue metric for each node (based on count of small eigenvalues)
        - Overall eigenvalue distribution metric
    """
    # Calculate the number of eigenvalues below threshold
    small_eigv_count = np.sum(eigvals < threshold)
    # Assign a metric to each node based on the proportion of small eigenvalues
    n = len(eigvals)
    node_eigv_metric = np.ones(n) * (small_eigv_count / n)
    # Coefficient of variation (std/mean) of eigenvalues as overall metric
    if np.mean(eigvals) > 0:
        overall_metric = np.std(eigvals) / np.mean(eigvals)
    else:
        overall_metric = np.std(eigvals)
    return overall_metric, node_eigv_metric

###############################################
# 4. Unified Uncertainty Score
###############################################
def compute_unified_uncertainty(ds, deg_vals, eigv_metric=None):
    """
    Normalization process:
    - Eccentricity: smaller is more reliable, so subtract from 1
    - Degree uncertainty: smaller is more reliable, so subtract from 1
    - Eigenvalue metric: smaller is more reliable, so subtract from 1
    """
    # Normalize eccentricity
    norm_ds = 1 - (ds - ds.min()) / (ds.max() - ds.min() + 1e-8)
    # Normalize degree uncertainty
    norm_deg = 1 - (deg_vals - deg_vals.min()) / (deg_vals.max() - deg_vals.min() + 1e-8)
    
    if eigv_metric is not None:
        # Normalize eigenvalue metric
        norm_eigv = 1 - (eigv_metric - eigv_metric.min()) / (eigv_metric.max() - eigv_metric.min() + 1e-8)
        # Calculate average of three metrics
        unified_score = (norm_ds + norm_deg + norm_eigv) / 3
        return norm_ds, norm_deg, norm_eigv, unified_score
    else:
        # Original calculation method, without eigenvalue consideration
        unified_score = (norm_ds + norm_deg) / 2
        return norm_ds, norm_deg, unified_score

###############################################
# 5. Main experiment: Compare 'jaccard' and 'agreement_w'
###############################################

# Create folder for saving visualization results
def create_vis_folder():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"visualization_results_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def analyze_spectral_eigv(W, mode_name, save_folder):
    """Analyze and visualize spectral eigenvalue distribution"""
    L = get_L_mat(W, symmetric=True)
    eigvals, eigvecs = get_eig(L)
    
    return eigvals, eigvecs

def compute_and_visualize(W, mode_name, save_folder, answers_labels=None):
    # 1) Spectral analysis
    eigvals, eigvecs = analyze_spectral_eigv(W, mode_name, save_folder)
    
    # 2) Eccentricity
    overall_ecc, ds = get_eccentricity(W, eigv_threshold=0.9)
    # 3) Degree Uncertainty
    deg_mean, deg_vals = get_degreeuq(W)
    # 4) Eigenvalue related metrics
    overall_eigv_metric, node_eigv_metric = get_eigv_metric(eigvals, threshold=0.9)
    # 5) Unified Uncertainty Score
    norm_ds, norm_deg, norm_eigv, unified_score = compute_unified_uncertainty(ds, deg_vals, eigv_metric=node_eigv_metric)
    
    print(f"\n----- {mode_name} Mode Results -----")
    print("Per-node Eccentricity:", ds)
    print("Overall Eccentricity:", overall_ecc)
    print("Per-node Degree Uncertainty:", deg_vals)
    print("Degree Uncertainty Mean:", deg_mean)
    print("Per-node Eigenvalue Metric:", node_eigv_metric)
    print("Overall Eigenvalue Metric:", overall_eigv_metric)
    print("Normalized Eccentricity:", norm_ds)
    print("Normalized Degree Uncertainty:", norm_deg)
    print("Normalized Eigenvalue Metric:", norm_eigv)
    print("Unified Uncertainty Score:", unified_score)

    # UMAP visualization
    features = np.column_stack((ds, deg_vals, node_eigv_metric))
    reducer = umap.UMAP(n_neighbors=3, min_dist=0.1, metric='euclidean', random_state=42)
    embedding = reducer.fit_transform(features)
    
def read_original_content(file_id):
    """Read original file content"""
    original_folder = '/Users/moonuke/Documents/Dataset/UQD/SWE-bench_md'
    file_path = os.path.join(original_folder, f"{file_id}.md")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"Warning: Cannot find original file {file_path}")
        return "Original file content not found"


def get_multiple_rephrased_results_from_lists(file_id):
    file_path = '/Users/moonuke/Documents/Dataset/UQD/SWE-bench_rephrased_results.json'

    # Read entire JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Get first record
    first_item = data[0]
    # Get first key-value pair
    first_key = list(first_item.keys())[0]
    first_value = first_item[first_key]

    # Parse inner JSON string
    inner_data = json.loads(first_value)

    print("First record ID:", first_key)

    # Read original file content
    original_content = read_original_content(first_key)
    print(f"Original content length: {len(original_content)} characters")
    print(f"Original content: {original_content}")

    # Extract LLM answers
    rephrased_answers = inner_data.get("rephrased_issue_descriptions", [])
    print(f"Total {len(rephrased_answers)} rephrased answers")

    # Add original content to the beginning of answers list
    answers = [original_content] + rephrased_answers
    n = len(answers)

    # Create labels list for visualization
    answers_labels = ["Original"] + [f"Rephrase{i+1}" for i in range(len(rephrased_answers))]

    # Print first few characters of first few answers
    for i, ans in enumerate(answers[1:6]):
        print(f"File length: {len(ans)}")
        print(f"Answer {i} : {ans[:]}...")

    # Create folder for saving results
    vis_folder = create_vis_folder()
    print(f"Saving visualization results to: {vis_folder}")
    
    # Jaccard mode
    print("=== Jaccard Mode ===")
    jaccard_mat = compute_jaccard_matrix(answers)
    print("Jaccard matrix:\n", jaccard_mat)
    
    # Agreement_w mode
    print("\n=== Agreement_w Mode ===")
    # Use numpy instead of torch
    logits = np.zeros((n, n, 3), dtype=np.float32)
    for i in range(n):
        for j in range(n):
            logits[i, j, 0] = 0.0
            logits[i, j, 1] = 0.5
            logits[i, j, 2] = float(jaccard_mat[i, j]) * 5.0
    
    agreement_w_mat = get_affinity_mat(logits, mode='agreement_w', temp=1.0, symmetric=True)
    print("Agreement_w matrix:\n", agreement_w_mat)
    
    # Calculate and visualize results for both modes
    compute_and_visualize(jaccard_mat, "Jaccard", vis_folder, answers_labels)
    compute_and_visualize(agreement_w_mat, "Agreement_w", vis_folder, answers_labels) 

def get_multiple_rephrased_results_from_multiple_rephrased(file_id=None):
    file_path = '/Users/moonuke/Documents/Dataset/UQD/SWE-bench_rephrased_results_multitime.json'

    # Read entire JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # If file_id not specified, use base_id from first entry
    if file_id is None:
        # Find first entry and extract base ID (remove suffix _0 to _4)
        first_key = list(data[0].keys())[0]
        base_id = first_key.rsplit('_', 1)[0]  # Remove last underscore and content after it
    else:
        base_id = file_id
    
    print(f"Base ID: {base_id}")
    
    # Read original file content
    original_content = read_original_content(base_id)
    print(f"Original content length: {len(original_content)} characters")
    
    # Extract all rephrased results with same base_id but different suffixes
    rephrased_answers = []
    for item in data:
        for key, value in item.items():
            # Check if key starts with base_id and has _number suffix
            if key.startswith(base_id + '_') and key[len(base_id)+1:].isdigit():
                # Value is directly the rephrased text
                rephrased_answers.append(value)
    
    print(f"Found {len(rephrased_answers)} rephrased answers")
    
    # Add original content to the beginning of answers list
    answers = [original_content] + rephrased_answers
    n = len(answers)
    
    # Create labels list for visualization
    answers_labels = ["Original"] + [f"Rephrase{i+1}" for i in range(len(rephrased_answers))]
    
    # Print first few characters of first few answers
    for i, ans in enumerate(answers[:min(6, len(answers))]):
        print(f"File length: {len(ans)}")
        # print(f"Answer {i} : {ans[:100]}...")
    
    # Create folder for saving results
    vis_folder = create_vis_folder()
    print(f"Saving visualization results to: {vis_folder}")
    
    # Jaccard mode
    print("=== Jaccard Mode ===")
    jaccard_mat = compute_jaccard_matrix(answers)
    print("Jaccard matrix:\n", jaccard_mat)
    
    # Agreement_w mode
    print("\n=== Agreement_w Mode ===")
    # Use numpy instead of torch
    logits = np.zeros((n, n, 3), dtype=np.float32)
    for i in range(n):
        for j in range(n):
            logits[i, j, 0] = 0.0
            logits[i, j, 1] = 0.5
            logits[i, j, 2] = float(jaccard_mat[i, j]) * 5.0
    
    agreement_w_mat = get_affinity_mat(logits, mode='agreement_w', temp=1.0, symmetric=True)
    print("Agreement_w matrix:\n", agreement_w_mat)
    
    # Calculate and visualize results for both modes
    compute_and_visualize(jaccard_mat, "Jaccard", vis_folder, answers_labels)
    compute_and_visualize(agreement_w_mat, "Agreement_w", vis_folder, answers_labels) 

def process_all_file_ids():
    """
    Process all file_ids in SWE-bench_rephrased_results_multitime.json,
    calculate Eccentricity and Degree Uncertainty metrics for each file_id,
    and save results to JSON file.
    """
    file_path = '/Users/moonuke/Documents/Dataset/UQD/SWE-bench_rephrased_results_multitime.json'
    
    # Read JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Dictionary to store all results
    all_results = {}
    
    # Get all unique base_ids
    base_ids = set()
    for item in data:
        for key in item.keys():
            base_id = key.rsplit('_', 1)[0]
            base_ids.add(base_id)
    
    print(f"Found {len(base_ids)} unique base_ids")
    
    # Process each base_id
    for base_id in base_ids:
        print(f"\nProcessing base_id: {base_id}")
        
        # Read original file content
        original_content = read_original_content(base_id)
        
        # Extract all rephrased results with same base_id but different suffixes
        rephrased_answers = []
        for item in data:
            for key, value in item.items():
                if key.startswith(base_id + '_') and key[len(base_id)+1:].isdigit():
                    rephrased_answers.append(value)
        
        # Add original content to the beginning of answers list
        answers = [original_content] + rephrased_answers
        n = len(answers)
        
        # Calculate Jaccard matrix
        jaccard_mat = compute_jaccard_matrix(answers)
        
        # Calculate Agreement_w matrix
        logits = np.zeros((n, n, 3), dtype=np.float32)
        for i in range(n):
            for j in range(n):
                logits[i, j, 0] = 0.0
                logits[i, j, 1] = 0.5
                logits[i, j, 2] = float(jaccard_mat[i, j]) * 5.0
        
        agreement_w_mat = get_affinity_mat(logits, mode='agreement_w', temp=1.0, symmetric=True)
        
        # Calculate metrics
        # Jaccard mode
        _, ds_jaccard = get_eccentricity(jaccard_mat, eigv_threshold=0.9)
        deg_mean_jaccard, deg_vals_jaccard = get_degreeuq(jaccard_mat)
        
        # Agreement_w mode
        _, ds_agreement = get_eccentricity(agreement_w_mat, eigv_threshold=0.9)
        deg_mean_agreement, deg_vals_agreement = get_degreeuq(agreement_w_mat)
        
        # Store results
        all_results[base_id] = {
            "jaccard": {
                "mat": jaccard_mat.tolist(),
                "per_node_eccentricity": ds_jaccard.tolist(),
                "per_node_degree_uncertainty": deg_vals_jaccard.tolist(),
                "overall_eccentricity": float(np.linalg.norm(ds_jaccard, ord=2)),
                "degree_uncertainty_mean": float(deg_mean_jaccard)
            },
            "agreement_w": {
                "mat": agreement_w_mat.tolist(),
                "per_node_eccentricity": ds_agreement.tolist(),
                "per_node_degree_uncertainty": deg_vals_agreement.tolist(),
                "overall_eccentricity": float(np.linalg.norm(ds_agreement, ord=2)),
                "degree_uncertainty_mean": float(deg_mean_agreement)
            }
        }
    
    # Save results to JSON file
    output_file = 'all_file_ids_input_eccentricity_degree_uncertainty.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")

if __name__ == '__main__':
    process_all_file_ids()