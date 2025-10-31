
from openai import OpenAI
import os
import json
from pydantic import BaseModel
from typing import List
from datasets import load_dataset
import requests

# OpenAI settings
OPENAI_API_KEY = "add openai key here"
GPT_MODEL = "o4-mini"

# Claude settings
OPENROUTER_API_KEY = "add openrouter api key here"
OPENROUTER_MODEL = "anthropic/claude-sonnet-4"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

class AnalysisResult(BaseModel):
    # Section 1: Issue Description Quality Assessment
    q1_1_is_well_specified: int  
    q1_2_explanation: str  
    
    # Section 2: Difficulty and Feasibility Assessment
    q2_1_difficulty: int  
    q2_2_explanation: str  
    q2_3_other_issues: int  
    q2_4_other_notes: str  
    q2_5_confidence: int  
    
    # Solution Effectiveness Analysis (new dimensions)
    q3_1_bug_fixing_score: int  # 0-2
    q3_2_execution_summary: str  # ~100 words
    q3_3_critical_trajectory_issues: int  # 0-1
    q3_4_potential_improvements: str  # minimum 100 characters
    q3_5_information_adequacy_assessment: int  # -2, -1, or 0


def get_tool_response(response):
    tool_call = response.choices[0].message.tool_calls[0]
    tool_args = json.loads(tool_call.function.arguments)
    return tool_args

def get_model_response(prompt, schema, model_type="gpt", max_retries=3):
    for attempt in range(max_retries):
        try:
            if model_type == "gpt":
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=GPT_MODEL,
                    messages=prompt,
                    functions=schema,
                )
                
                if schema is not None:
                    function_args = response.choices[0].message.function_call.arguments
                    if function_args and function_args.strip():
                        return function_args
                return response.choices[0].message.content or ""
                
            elif model_type == "openrouter":
                client = OpenAI(
                    base_url=OPENROUTER_API_URL,
                    api_key=OPENROUTER_API_KEY,
                )

                # Convert functions schema to tools schema
                tools = [{
                    "type": "function",
                    "function": {
                        "name": schema[0]["name"],
                        "description": schema[0]["description"],
                        "parameters": schema[0]["parameters"]
                    }
                }]

                # First API call with tools
                response = client.chat.completions.create(
                    model=OPENROUTER_MODEL,
                    messages=prompt,
                    tools=tools
                )

                # Check if we got a tool call
                if response.choices[0].message.tool_calls:
                    return get_tool_response(response)
                return response.choices[0].message.content or ""
            
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print("All attempts failed, returning empty string")
                return ""
            continue
    
    return ""



def load_json_previous_judgments(json_file_path):
    """load previous judgments from JSON file"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        previous_judgments = {}
        for item in data:
            for instance_id, judgment_response in item.items():
                try:
                    judgment_data = json.loads(judgment_response)
                    previous_judgments[instance_id] = {
                        'instance_id': instance_id,
                        'q1_1_is_well_specified': judgment_data.get('q1_1_is_well_specified', 'N/A'),
                        'q1_2_explanation': judgment_data.get('q1_2_explanation', 'N/A'),
                        'q2_1_difficulty': judgment_data.get('q2_1_difficulty', 'N/A'),
                        'q2_2_explanation': judgment_data.get('q2_2_explanation', 'N/A'),
                        'q2_3_other_issues': judgment_data.get('q2_3_other_issues', 'N/A'),
                        'q2_4_other_notes': judgment_data.get('q2_4_other_notes', 'N/A'),
                        'q2_5_confidence': judgment_data.get('q2_5_confidence', 'N/A')
                    }
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"parse judgment data failed {instance_id}: {e}")
                    previous_judgments[instance_id] = {
                        'instance_id': instance_id,
                        'raw_response': judgment_response,
                        'parse_error': str(e)
                    }
        
        return previous_judgments
    except Exception as e:
        print(f"load JSON file failed: {e}")
        return {}


def load_trajectory_reports(trajectory_folder, instance_id, segment_evaluation=False):
    """load trajectory reports, return each file's independent content for separate evaluation"""
    trajectory_files = []
    
    # build instance_id folder path
    instance_folder = os.path.join(trajectory_folder, instance_id, "README")
    
    if not os.path.exists(instance_folder):
        print(f"trajectory folder not found: {instance_folder}")
        return []
    
    try:
        # load analysis_report_full.md
        analysis_report_path = os.path.join(instance_folder, "analysis_report_full.md")
        if os.path.exists(analysis_report_path):
            with open(analysis_report_path, 'r', encoding='utf-8') as f:
                analysis_content = f.read()
                trajectory_files.append({
                    'file_name': 'analysis_report_full.md',
                    'content': analysis_content
                })
        
        if segment_evaluation:
            # load all segment files (segment_1.md, segment_2.md, etc.)
            segment_files = glob.glob(os.path.join(instance_folder, "analysis_report_segment_*.md"))
            segment_files.sort()  # ensure sorted
            
            for segment_file in segment_files:
                segment_name = os.path.basename(segment_file)
                with open(segment_file, 'r', encoding='utf-8') as f:
                    segment_content = f.read()
                    trajectory_files.append({
                        'file_name': segment_name,
                        'content': segment_content
                    })
        
        return trajectory_files
            
    except Exception as e:
        print(f"load trajectory report failed {instance_id}: {e}")
        return []


def parse_nested_json(data):
    result = {}
    for item in data:
        for key, value in item.items():
            try:
                result[key] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                result[key] = value
    return result 

def load_file(filename):
    with open(filename, 'r') as f:
        return json.load(f) if filename.endswith('.json') else f.read()



def system_prompt(file_content, example_content, previous_judgments=None, execution_trajectory=None):

    prompt = [
        {
            "role": "user",
            "content": """You are an experienced software engineer conducting an critical analysis on GitHub issue resolution. Your task is to re-evaluate issue descriptions and assess the impact of different information components on problem-solving effectiveness."""
        },
        {
            "role": "user",
            "content": f"""
            ## Task Overview
            You are evaluating GitHub issues from open-source Python repositories. Each issue has:
            1. Original issue description 
            2. Previous LLM evaluation of the description
            3. Current LLM agent execution trajectory and results
            
            Your goal is to:
            - Re-assess the issue description quality based on the execution results
            - Determine if previous judgments should be updated
            - Evaluate the solution effectiveness
            - Identify if there is missing critical information to solve the issue
            
            ## Issue Description to Evaluate
            {file_content}

            ## Evaluation Framework

            ### Section 1: Issue Description Quality Assessment
            
            **Context**: You are an experienced software engineer tasked with creating a PR to resolve this GitHub issue. You have full codebase access but cannot ask for clarification - you must work exclusively from the provided information.

            Is the issue description well-specified enough for a meaningful attempt at a solution?
            Question 1.1
            ● 0: The issue is well-specified and it is clear what is required for a successful solution.
            ○ Example: pylint #5201 {example_content[0]}
            ● 1: There are some blanks to fill in about the issue, but there is a sensible interpretation of what is required for a successful solution.
            ○ Example: sympy #18030 {example_content[1]}
            ● 2: The issue is vague and there is room for ambiguity. It is unclear what a successful solution would look like.
            ○ Example: scikit-learn #14520 {example_content[2]}
            ● 3: It is almost impossible to understand what you are being asked to do without further information.
            ○ Example: pylint #5743 {example_content[3]}

            Please explain your choice above. Include references to specific filenames, function/class names, or lines of code where relevant.
            Question 1.2
            [Free text, minimum 100 characters]


            ### Section 2: Difficulty and Feasibility Assessment
            You will consider the GitHub issue again and answer a final set of questions. You may navigate back to previous sections to see the issue and patches.
            
            Difficulty
            We wish to understand how difficult this issue is to solve.
            How long would it take (for an experienced software engineer who had a few hours to familiarize themselves with the codebase) to understand the problem described in the GitHub issue, arrive at a solution and write the code for a solution?
            Note: If the issue text was previously too ambiguous to solve at all, you may assume that the problem has been clarified sufficiently such that the high-level requirements for the solution are clear ("what"), but the specifics about the solution are left to the engineer to figure out ("how").
           
            Question 2.1
            ● 0: <15 min fix
            ○ e.g., a trivial change adding some assertions to a function
            ● 1: 15 min - 1 hour
            ○ e.g., a small change that requires a bit of thought
            ● 2: 1-4 hours
            ○ e.g., substantially rewriting a function or editing multiple files
            ● 3: 4 hours
            ○ e.g., a very esoteric issue that clearly requires a substantial amount of research to fix, changing >100 lines of code
            
            Question 2.2
            Explain why you chose the difficulty level above.
            
            Question 2.3
            Are there any other major issues that haven't been covered? i.e. Any other reasons this sample should not be used in our setup for evaluating coding ability.
            ● 0: No
            ● 1: Yes

            Question 2.4
            Do you have any other notes you wish to add? If you answered 'Yes' to the previous question 2.3, please explain here.
            [Free text, minimum 100 characters]

            Question 2.5 
            Confidence
            Overall, how confident are you in the answers you have given for this sample?
            [1,2,3,4,5]

            
            ## Previous Evaluation of Description Results
            {previous_judgments if previous_judgments else "No previous evaluation available."}

            ## Current Execution Results
            {execution_trajectory if execution_trajectory else "No execution trajectory available."}

            
            ## Re-evaluation Task
            
            Based on the up to date execution results, provide updated assessments for Questions 1.1-2.5 and answer the following:

            ### Section 3: Solution Effectiveness Analysis
            
            Question 3.1: Bug Fixing Score (0-2)
            • 0: No changes or incorrect changes made
            • 1: Partially correct changes that address some aspects
            • 2: Correct changes that fully resolve the issue

            Question 3.2: Execution Summary
            Summarize the agent's execution trajectory and key findings in approximately 100 words.

            Question 3.3: Critical Trajectory Issues (0-1)
            • 0: No critical issues in the execution approach
            • 1: Significant problems in the execution strategy or implementation

            Question 3.4: Potential Improvements
            Describe specific ways the solution approach could be enhanced or what alternative strategies might be more effective.
            [Minimum 100 characters]

            Question 3.5: Information Adequacy Assessment
            Evaluate if additional information from the issue reporter would help:
            • **-1**: Need more reproduction steps/examples
            • **-2**: Need more runtime error details/stack traces  
            • **0**: Current information is sufficient

            ## Output Format
            Provide your analysis in the structured format defined by the function schema, ensuring all numerical ratings and text explanations are included.
            """
        }
    ]
    
    schema = [{
        "name": "analyze_issue_description_and_difficulty",
        "description": "Analyze issue description and difficulty of the issue",
        "parameters": AnalysisResult.model_json_schema()
    }]
    
    return prompt, schema

def save_results(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

def load_existing_results(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_processed_instance_ids(results):
    processed_ids = set()
    for result in results:
        for instance_id in result.keys():
            processed_ids.add(instance_id)
    return processed_ids


def get_target_instance_ids(folder_path):
    """get instance_id list from target folder"""
    instance_ids = set()
    
    folder_name = folder_path.split("/")[-1]
    if folder_name == 'og':
        actual_folder_path = folder_path.replace('og', 'both_rephrased')
    else:
        actual_folder_path = folder_path
    
    if not os.path.exists(actual_folder_path):
        print(f"target folder not found - {actual_folder_path}")
        return instance_ids
    
    try:
        for filename in os.listdir(actual_folder_path):
            if filename.endswith('.md'):
                # remove .md suffix
                instance_id = filename[:-3]
                instance_ids.add(instance_id)
    except Exception as e:
        print(f"read folder failed {actual_folder_path}: {e}")
    
    return instance_ids

def main(target_folder, model_type="gpt", save_file_name="SWE-bench_LLM_as_judge_for_description.json", trajectory_folder=None, previous_judgments_path=None, folder='og'):
    example_name = ['pylint-dev__pylint-5201', 'sympy__sympy-18030', 'scikit-learn__scikit-learn-14520', 'pylint-dev__pylint-5743']
    responses = []
    example_content = []
    swebench_df = []

    previous_judgments_data = load_json_previous_judgments(previous_judgments_path)
    print(f"loaded {len(previous_judgments_data)} previous judgments")

    target_instance_ids = get_target_instance_ids(target_folder)

    existing_results = load_existing_results(save_file_name)
    processed_instance_ids = get_processed_instance_ids(existing_results)
    responses = existing_results 
    
    print(f"Found {len(processed_instance_ids)} processed instances")

    swebench = load_dataset('princeton-nlp/SWE-bench', split='test')
    swebench_df = swebench.to_pandas()

    for example_name in example_name:
        example_content.append(swebench_df[swebench_df['instance_id'] == example_name]['problem_statement'].values[0])

    print(f"Starting processing with model: {model_type}")
    for index, row in swebench_df.iterrows():
        instance_id = row['instance_id']
        
        if instance_id not in target_instance_ids or instance_id in processed_instance_ids:
            print(f"Skipping processed instance: {instance_id}")
            continue

        if folder == 'og':
            problem_statement = row['problem_statement']
        else:
            ablation_content = load_file(os.path.join(target_folder, f"{instance_id}.md"))
            problem_statement = ablation_content 
        
        # get previous judgments
        previous_judgment = previous_judgments_data.get(instance_id, "No previous judgment available for this instance.")
        # load trajectory files
        trajectory_files = load_trajectory_reports(trajectory_folder, instance_id)
        
        if not trajectory_files:
            print(f"{instance_id} - no trajectory files found")
            continue

        # evaluate each trajectory file
        instance_responses = {}
        
        for trajectory_file in trajectory_files:
            file_name = trajectory_file['file_name']
            file_content = trajectory_file['content']
            
            print(f"processing {instance_id} - {file_name}")
            
            prompt, schema = system_prompt(problem_statement, example_content, previous_judgment, file_content)
            response = get_model_response(prompt, schema)
            
            if response:
                instance_responses[file_name] = response
                print(f"{instance_id} - {file_name} done")
            else:
                print(f"{instance_id} - {file_name} failed - empty response")
        
        # save all responses for this instance
        if instance_responses:
            save_respone = {instance_id: instance_responses}
            responses.append(save_respone)
            print(f"{instance_id} all files processed, {len(instance_responses)} files")
        else:
            print(f"{instance_id} failed - all files have no response")

        # save each instance response to avoid data loss
        save_results(responses, save_file_name)


if __name__ == "__main__":

    base_folder = '/Users/moonuke/Documents/Dataset/UQD/release/datasets/SWE-bench_verified_ablation_descriptions'
    # base_folder = ' /Users/moonuke/Documents/Dataset/UQD/release/trajectories/claude4'
    target_folders = [
        # 'og',
        'both_removed',
        'both_rephrased',
        'reproduction_removed',
        # 'reproduction_rephrased',
        'runtime_error_removed',
        # 'runtime_error_rephrased'
    ]
    

    for folder in target_folders:
        target_folder = os.path.join(base_folder, folder)
        print(f"\starget folder: {folder}")

        # trajectory_folder = f'/Users/moonuke/Documents/Dataset/UQD/o3mini_res/CodeActAgent/o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_{folder}_all/llm_completions'
        # previous_judgments_path = f'/Users/moonuke/Documents/Dataset/UQD/release/judgements/claude4/SWE-bench_LLM_as_judge_for_description_claude4_{folder}.json'
        trajectory_folder = f'/Users/moonuke/Documents/Dataset/UQD/release/trajectories/claude4/claude-sonnet-4_maxiter_100_N_v0.48.0-no-hint-run_1_{folder}/llm_completions'
        previous_judgments_path = f'/Users/moonuke/Documents/Dataset/UQD/release/judgements/claude4/SWE-bench_LLM_as_judge_for_description_claude4_{folder}.json'

        save_file_name = f"SWE-bench_LLM_as_judge_for_description_claude4_{folder}.json"
        main(target_folder=target_folder, model_type="openrouter", save_file_name=save_file_name, trajectory_folder=trajectory_folder, previous_judgments_path=previous_judgments_path, folder=folder)
        print(f"done\n")