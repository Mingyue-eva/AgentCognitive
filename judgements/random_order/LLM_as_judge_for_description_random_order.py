
from openai import OpenAI
import os
import json
from pydantic import BaseModel
from typing import List
from datasets import load_dataset
import requests
import random

# OpenAI settings
OPENAI_API_KEY = "key here"
GPT_MODEL = "gpt-4.1" #gpt-4.1 o4-mini

# Claude settings
OPENROUTER_API_KEY = "key here"
OPENROUTER_MODEL = "anthropic/claude-sonnet-4"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

class AnalysisResult(BaseModel):
    # A. Problem Statement Analysis
    q1_1_is_well_specified: int  
    q1_2_explanation: str  
    q2_1_difficulty: int  
    q2_2_explanation: str  
    q2_3_other_issues: int  
    q2_4_other_notes: str  
    q2_5_confidence: int  

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

def randomize_options(options, labels):
    """Randomize the order of options and return both randomized options and mapping"""
    combined = list(zip(options, labels))
    random.shuffle(combined)
    randomized_options, randomized_labels = zip(*combined)
    
    # Create mapping from randomized position to original value
    original_to_randomized = {}
    for i, label in enumerate(labels):
        randomized_pos = randomized_labels.index(label)
        original_to_randomized[i] = randomized_pos
    
    return list(randomized_options), list(randomized_labels), original_to_randomized

def system_prompt(file_content, example_content, Gold_Patch, Test_Patch):
    # Define specification options and randomize their order
    spec_options = [
        "The issue is well-specified and it is clear what is required for a successful solution.",
        "There are some blanks to fill in about the issue, but there is a sensible interpretation of what is required for a successful solution.",
        "The issue is vague and there is room for ambiguity. It is unclear what a successful solution would look like.",
        "It is almost impossible to understand what you are being asked to do without further information."
    ]
    spec_examples = [
        f"pylint #5201 {example_content[0]}",
        f"sympy #18030 {example_content[1]}",
        f"scikit-learn #14520 {example_content[2]}",
        f"pylint #5743 {example_content[3]}"
    ]
    spec_labels = [0, 1, 2, 3]
    
    randomized_spec_options, randomized_spec_labels, spec_mapping = randomize_options(spec_options, spec_labels)
    # Match examples with their corresponding randomized options
    randomized_spec_examples = []
    for label in randomized_spec_labels:
        original_index = spec_labels.index(label)
        randomized_spec_examples.append(spec_examples[original_index])
    
    # Define difficulty options and randomize their order
    diff_options = [
        "<15 min fix",
        "15 min - 1 hour", 
        "1-4 hours",
        "4 hours"
    ]
    diff_examples = [
        "e.g., a trivial change adding some assertions to a function",
        "e.g., a small change that requires a bit of thought",
        "e.g., substantially rewriting a function or editing multiple files", 
        "e.g., a very esoteric issue that clearly requires a substantial amount of research to fix, changing >100 lines of code"
    ]
    diff_labels = [0, 1, 2, 3]
    
    randomized_diff_options, randomized_diff_labels, diff_mapping = randomize_options(diff_options, diff_labels)
    # Match examples with their corresponding randomized options
    randomized_diff_examples = []
    for label in randomized_diff_labels:
        original_index = diff_labels.index(label)
        randomized_diff_examples.append(diff_examples[original_index])
    
    # Build specification section with randomized options
    spec_section = ""
    for i, (option, example, label) in enumerate(zip(randomized_spec_options, randomized_spec_examples, randomized_spec_labels)):
        spec_section += f"● {label}: {option}\n"
        spec_section += f"○ Example: {example}\n"
    
    # Build difficulty section with randomized options  
    diff_section = ""
    for i, (option, example, label) in enumerate(zip(randomized_diff_options, randomized_diff_examples, randomized_diff_labels)):
        diff_section += f"● {label}: {option}\n"
        diff_section += f"○ {example}\n"

    prompt = [
        {
            "role": "system",
            "content": "You are an experienced software engineer tasked with judging whether issue descriptions are well-specified and suitable for use in our benchmark, and assessing their difficulty."
        },
        {
            "role": "user",
            "content": f"""
            We have a dataset of GitHub issues from various open-source Python repositories. Each issue comes with a PR that successfully solves the issue described. Each PR consists of 2 parts: 
            (1) code that resolves the issue 
            (2) changes to the test files of the repository, which check whether the issue has been resolved.
            
            We intend to use samples in this dataset as a benchmark for coding ability: For each sample, we give an engineer the issue text and ask them to write code to resolve the issue (without revealing the solution from the original PR). Then, we apply the test files from the original PR to their code and run the tests to check whether their solution passes.   
            
            Importantly, this setup assumes that:
            ● The issue description is sufficiently well-specified to understand what the problem is, and what the correct solution should look like.

            In this task, you will help to check those assumptions and identify which issue samples are suitable for use in our benchmark.

            
            Please take a moment to read the issue description below. 
            IMPORTANT: Do not click through on any external links, and do not read the discussion below the GitHub issue. Our setup will only provide the main issue text as shown below, so please answer the questions on the basis of only the text shown here.
            
            {file_content}

            Section 1 - Issue Description
            How well-specified is the issue text?
            Imagine that you are an experienced software engineer who has been instructed to create a PR that successfully resolves the above GitHub issue. You have full access to the codebase, and can see the issue description as it is above. But you are not able to ask for clarification and would need to work exclusively from this information. 
            
            Is the issue description well-specified enough for a meaningful attempt at a solution?
            Question 1.1
            {spec_section}
            Please explain your choice above. Include references to specific filenames, function/class names, or lines of code where relevant.
            Question 1.2
            [Free text, minimum 100 characters]

            (1) code that resolves the issue 
            (Gold Patch of the issue resolved by the PR)
            {Gold_Patch}
            
            (2) changes to the test files of the repository, which check whether the issue has been resolved.
            (Test Patch of the issue resolved by the PR)    
            {Test_Patch}

            Section 2
            You will consider the GitHub issue again and answer a final set of questions. You may navigate back to previous sections to see the issue and patches.
            
            Difficulty
            We wish to understand how difficult this issue is to solve.
            How long would it take (for an experienced software engineer who had a few hours to familiarize themselves with the codebase) to understand the problem described in the GitHub issue, arrive at a solution and write the code for a solution?
            Note: If the issue text was previously too ambiguous to solve at all, you may assume that the problem has been clarified sufficiently such that the high-level requirements for the solution are clear ("what"), but the specifics about the solution are left to the engineer to figure out ("how").
           
            Question 2.1
            {diff_section}
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
            """
        }
    ]
    
    schema = [{
        "name": "analyze_issue_description_and_difficulty",
        "description": "Analyze issue description and difficulty of the issue",
        "parameters": AnalysisResult.model_json_schema()
    }]
    
    return prompt, schema, spec_mapping, diff_mapping

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

def main(model_type="gpt", save_file_name="SWE-bench_LLM_as_judge_for_description.json"):
    example_name = ['pylint-dev__pylint-5201', 'sympy__sympy-18030', 'scikit-learn__scikit-learn-14520', 'pylint-dev__pylint-5743']
    responses = []
    example_content = []
    swebench_df = []

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
        
        if instance_id in processed_instance_ids:
            print(f"Skipping processed instance: {instance_id}")
            continue
            
        problem_statement = row['problem_statement']
        Gold_Patch = row['patch']
        Test_Patch = row['test_patch']

        prompt, schema, spec_mapping, diff_mapping = system_prompt(problem_statement, example_content, Gold_Patch, Test_Patch)
        response = get_model_response(prompt, schema, model_type=model_type)
        
        if response:
            # Include randomization mappings in the response for analysis
            save_response = {
                instance_id: {
                    "response": response,
                    "spec_mapping": spec_mapping,  # Maps original position to randomized position
                    "diff_mapping": diff_mapping   # Maps original position to randomized position
                }
            }
            responses.append(save_response)
            print(f"Successfully processed {instance_id}")
        else:
            print(f"Failed to process {instance_id} - empty response")

        save_results(responses, save_file_name)

if __name__ == "__main__":
    save_file_name = "SWE-bench_LLM_as_judge_for_description_gpt4.1_og_random_order.json"
    main(model_type="gpt", save_file_name=save_file_name) # openrouter or "gpt"
