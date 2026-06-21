import json
import re
import os
import csv
from datetime import datetime

# Global debug switch
DEBUG_MODE = False

def set_debug_mode(enabled):
    """Set debug mode"""
    global DEBUG_MODE
    DEBUG_MODE = enabled

def debug_print(message):
    """Conditional debug printing"""
    if DEBUG_MODE:
        print(message)

def is_actual_error(tool_name, tool_input, output):
    """
    Determine if the tool execution output is an actual error
    """
    if not output:
        return False
    
    output_str = str(output).strip()
    output_lower = output_str.lower()
    
    # If output is empty, not considered an error
    if not output_str:
        return False
    
    # Check if it's a tool execution level error (rather than an error in code content)
    # If it's a code view or edit operation and contains success indicators, not considered an error
    if re.search(r'here.*s the result of running.*cat', output_lower):
        return False  # This is viewing code content, regardless of content it's not an error
    
    if 'has been edited' in output_lower or 'file created successfully' in output_lower:
        return False  # Edit successful, regardless of the content, it's not considered an error

    # Special handling for str_replace_editor
    if tool_name == "str_replace_editor":
        # Check for explicit success indicators
        success_indicators = [
            "has been edited",
            "File created successfully",
            "successfully created",
            "successfully modified",
            "successfully updated",
            "Applied edit to"
        ]
        
        if any(indicator in output_str for indicator in success_indicators):
            return False
        
        # Check if error is due to unmatched text (this is a real error)
        if "No replacement was performed" in output_str and "did not appear verbatim" in output_str:
            return True
        
        # Check for system errors like file not found
        if any(error in output_str for error in ["No such file or directory", "Permission denied", "cannot access"]):
            return True
        
        # If output only contains exception handling code (like except statements), not an error
        lines = output_str.split('\n')
        error_related_lines = []
        for line in lines:
            line = line.strip()
            if any(error_type in line for error_type in ['except ', 'try:', 'raise ', 'Error:', 'Exception:']):
                error_related_lines.append(line)
        
        # If all error-related lines are exception handling code, not an error
        if error_related_lines and all('except ' in line or 'try:' in line for line in error_related_lines):
            return False
        
        # Check for real Python error (with complete traceback)
        if "Traceback (most recent call last):" in output_str:
            return True
        
        # If output contains ERROR: but is followed by exception handling code, not an error
        if "ERROR:" in output_str:
            error_parts = output_str.split("ERROR:")
            if len(error_parts) > 1:
                error_content = error_parts[1].strip()
                # If error content is just exception handling code, not an error
                if error_content.startswith('except ') or error_content.startswith('try:'):
                    return False
        
        return False
    
    # Special handling for execute_bash
    elif tool_name == "execute_bash":
        # If output is empty or minimal, usually indicates success
        if len(output_str.strip()) == 0:
            return False
        # Common success output patterns
        if re.search(r'^\s*$', output_str):  # Empty output
            return False
        
        # Check for explicit success indicators
        success_indicators = [
            "completed successfully",
            "operation completed",
            "finished successfully"
        ]
        
        if any(indicator in output_str for indicator in success_indicators):
            return False
        
        # Check for explicit command execution failure errors
        bash_errors = [
            "command not found",
            "No such file or directory",
            "Permission denied",
            "cannot access",
            "bash: ",
            "sh: ",
            "error:",
            "failed:",
            "Error:",
            "Failed:"
        ]
        
        # If output contains bash errors but also code content, needs further analysis
        has_bash_error = any(error in output_str for error in bash_errors)
        
        # If output looks like code content (contains Python code structure), not an error even with error keywords
        code_indicators = [
            "def ",
            "class ",
            "import ",
            "from ",
            "try:",
            "except ",
            "if __name__",
            "return ",
            "    #",  # Indented comment
            "    def",  # Indented function definition
            "    class",  # Indented class definition
        ]
        
        has_code_content = any(indicator in output_str for indicator in code_indicators)
        
        # If output is primarily code content, not an error
        if has_code_content:
            # Check if it's normal output from sed/cat commands
            lines = output_str.split('\n')
            code_lines = sum(1 for line in lines if any(indicator in line for indicator in code_indicators))
            total_lines = len([line for line in lines if line.strip()])
            
            # If most lines are code, not an error
            if total_lines > 0 and code_lines / total_lines > 0.3:
                return False
        
        # Only consider it an error if there's an explicit bash error and no code content
        if has_bash_error and not has_code_content:
            return True
        
        return False
    
    # General error patterns - only count as error in actual error context
    # Check if it's a real Python error (with complete traceback)
    if 'traceback (most recent call last):' in output_lower:
        return True
    
    # Error detection for other tools
    error_indicators = [
        "Error:",
        "ERROR:",
        "Failed:",
        "FAILED:",
        "Exception:",
        "command not found",
        "No such file or directory",
        "Permission denied"
    ]
    
    # Check for explicit error indicators
    if any(indicator in output_str for indicator in error_indicators):
        # Further check if it's error handling code rather than actual error
        if "except " in output_str or "try:" in output_str:
            # If it's Python exception handling code, not an error
            return False
        return True
    
    return False

def extract_info_from_json(json_file, output_dir, write_file=True):
    # Read JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract all information
    messages = []
    tool_results = []
    if 'messages' in data:
        for message in data['messages']:
            if message.get('role') == 'tool':
                # Tool execution results are in the tool role's content
                tool_results.append({
                    'name': message.get('name', 'Unknown'),
                    'content': message.get('content', '')
                })
            elif 'content' in message and message['content']:
                for content in message['content']:
                    if content['type'] == 'text':
                        messages.append({
                            'role': message.get('role', ''),
                            'content': content['text']
                        })
    
    # Generate README content
    readme_content = f"""# AI Conversation Analysis Report

## Tool Execution Analysis
Total tool executions: {len(tool_results)}

"""

    # Statistics
    total_executions = len(tool_results)
    failed_executions = 0
    failure_reasons = []
    execution_results = []  # Store status and error info for each execution

    for i, result in enumerate(tool_results, 1):
        # Add tool execution results
        readme_content += f"\n### TOOL EXECUTION #{i}\n"
        readme_content += f"Tool Name: {result['name']}\n"
        readme_content += "```\n"
        
        output = result['content']
        if isinstance(output, list):
            # If it's a list, extract text content
            text_parts = []
            for item in output:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
                else:
                    text_parts.append(str(item))
            output = "\n".join(text_parts)
        readme_content += str(output) + "\n"
        readme_content += "```\n"
        
        # Use intelligent error detection
        tool_name = result['name']
        error_details = []
        
        if is_actual_error(tool_name, "", str(output)):
            execution_status = "❌ Failed"
            failed_executions += 1
            
            # Extract error details - improve logic, avoid extracting exception handling code from code content
            output_lines = str(output).split('\n')
            
            # Find specific error information, but avoid extracting exception handling code from code content
            for line in output_lines:
                line_stripped = line.strip()
                line_lower = line_stripped.lower()
                
                # Skip code content lines (usually code content)
                if line_stripped.startswith('except ') or line_stripped.startswith('try:'):
                    continue
                    
                # Skip indented code lines (usually code content)
                if line.startswith('    ') or line.startswith('\t'):
                    continue
                
                # Only extract lines with actual error information
                if any(error in line_lower for error in ['error:', 'traceback (most recent call last):']):
                    error_details.append(f"- {line_stripped}")
                elif line_lower.startswith('no replacement was performed'):
                    error_details.append(f"- {line_stripped}")
                elif any(error in line_lower for error in ['no such file', 'permission denied', 'command not found']):
                    error_details.append(f"- {line_stripped}")
                    
            if not error_details:
                error_details.append(f"- Execution failed")
                
            failure_reasons.extend(error_details)
            
            readme_content += f"\nStatus: {execution_status}\n"
            readme_content += "\nError Details:\n"
            readme_content += "\n".join(error_details) + "\n"
        else:
            execution_status = "✅ Success"
            readme_content += f"\nStatus: {execution_status}\n"
        
        # Save execution results, using 1-based incrementing index
        execution_results.append({
            'tool_name': result['name'],
            'status': execution_status,
            'error_details': error_details,
            'content': str(output),
            'execution_number': i  # 1-based incrementing index
        })

    # Add summary information
    success_rate = ((total_executions - failed_executions) / total_executions * 100) if total_executions > 0 else 0
    readme_content += f"\n## Execution Summary\n"
    readme_content += f"- Total Executions: {total_executions}\n"
    readme_content += f"- Successful Executions: {total_executions - failed_executions}\n"
    readme_content += f"- Failed Executions: {failed_executions}\n"
    readme_content += f"- Success Rate: {success_rate:.2f}%\n"

    if failed_executions > 0:
        readme_content += "\n## Error Analysis\n"
        for reason in failure_reasons:
            readme_content += f"{reason}\n"

    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Save as README.md
    file_name = os.path.splitext(os.path.basename(json_file))[0] + '_analyze_trace.md'
    
    if write_file:
        readme_path = os.path.join(output_dir, file_name)
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"README.md generated in directory: {output_dir, file_name}")
    
    # Return execution results and statistics
    summary = {
        'total_executions': total_executions,
        'successful_executions': total_executions - failed_executions,
        'failed_executions': failed_executions,
        'success_rate': success_rate
    }
    return [output_dir, file_name, execution_results, summary]



def analyze_trace_execution_result(base_dir):
    # Get all JSON files in the directory
    json_files = []
    for file in os.listdir(base_dir):
        if file.endswith('.json'):
            full_path = os.path.join(base_dir, file)
            created_time = os.path.getmtime(full_path)
            json_files.append((created_time, full_path))
    
    # Sort by time to ensure consistent order
    json_files.sort(key=lambda x: x[0])

    if not json_files:
        print("No JSON files found")
        return None, None, None, None

    # Unified output directory
    output_dir = os.path.join(base_dir, 'README')

    # Analyze only the last JSON file (latest conversation history)
    last_json_path = json_files[-1][1]
    
    # Analyze the last JSON file
    try:
        result = extract_info_from_json(last_json_path, output_dir, write_file=True)
        if not result:
            return None, None, None, None
        
        # result structure: [output_dir, file_name, execution_results, summary]
        return result[0], result[1], result[2], result[3]
    except Exception as e:
        print(f"Error processing {last_json_path}: {e}")
        return None, None, None, None

class TraceNode:
    """Represents a node in the operation relationship tree"""
    def __init__(self, trace_type, operations, parent=None):
        self.type = trace_type  # Trace type
        self.operations = operations  # Sequence of operations
        self.parent = parent  # Parent node
        self.children = []  # Child nodes
        self.is_alternative = False  # Whether it's an alternative path (rollback modification)
        self.execution_status = None  # Execution status: success/failure
        self.error_details = []  # Error details
        self.tool_name = None  # Tool name
        self.execution_number = None  # Execution index
        
    def add_child(self, child):
        """Add a child node"""
        child.parent = self
        self.children.append(child)
        
    def get_modified_files(self):
        """Get the files modified by this node"""
        files = set()
        for op in self.operations:
            if op['tool'] == 'str_replace_editor' and op['args']['command'] == 'str_replace':
                files.add(op['args']['path'])
        return files

def build_trace_tree(traces, execution_results=None):
    """Build the operation relationship tree, based on rollback points
    
    Args:
        traces: List of traces, each containing purpose and operations
        execution_results: List of execution results
    
    Returns:
        root: Root node of the tree
    """
    if not traces:
        return None
    
    # Create execution result mapping
    execution_map = {}
    if execution_results:
        for result in execution_results:
            execution_map[result['execution_number']] = result
    
    # Identify rollback points (consistent with count_rollbacks function)
    rollback_trace_indices = []
    last_modification_index = -1
    last_failed_test_index = -1
    
    for i, trace in enumerate(traces):
        if trace['purpose'] == 'code_modification':
            last_modification_index = i
            # Reset failed test execution index, as logic restarts after code_modification
            last_failed_test_index = -1
        elif trace['purpose'] == 'test_execution':
            # Check if test_execution failed
            is_failed = False
            for operation in trace['operations']:
                exec_num = operation.get('execution_number')
                if exec_num and exec_num in execution_map:
                    result = execution_map[exec_num]
                    if "❌" in result['status']:
                        is_failed = True
                        break
            
            if is_failed:
                last_failed_test_index = i
                # If test_execution failed, reset modification index, as subsequent code_analysis should be based on test_execution failure
                last_modification_index = -1
            else:
                # If test_execution succeeded, reset failed index and modification index
                last_failed_test_index = -1
                last_modification_index = -1
        elif trace['purpose'] == 'code_analysis':
            if last_modification_index != -1:
                rollback_trace_indices.append(last_modification_index)
                last_modification_index = -1
            if last_failed_test_index != -1:
                rollback_trace_indices.append(last_failed_test_index)
                last_failed_test_index = -1
    
    # Create nodes for each operation
    all_nodes = []
    for trace in traces:
        for operation in trace['operations']:
            exec_num = operation.get('execution_number')
            
            # Create operation node
            node = TraceNode(trace['purpose'], [operation])
            node.execution_number = exec_num
            
            # Set execution status information
            if exec_num and exec_num in execution_map:
                result = execution_map[exec_num]
                node.execution_status = result['status']
                node.error_details = result['error_details']
                node.tool_name = result['tool_name']
            
            all_nodes.append(node)
    
    # Sort by execution index
    all_nodes.sort(key=lambda x: x.execution_number if x.execution_number else 0)
    
    if not all_nodes:
        return None
    
    # Convert trace-level rollback points to operation-level split points
    rollback_operation_points = []
    for trace_idx in rollback_trace_indices:
        if trace_idx < len(traces) and traces[trace_idx]['operations']:
            # Get execution index of the last operation in the trace
            last_op_in_trace = traces[trace_idx]['operations'][-1]
            rollback_operation_points.append(last_op_in_trace['execution_number'])
    
    rollback_operation_points.sort()
    
    # Build tree structure based on rollback points
    root = all_nodes[0]
    
    if not rollback_operation_points:
        # No rollback points, build simple linear tree
        for i in range(1, len(all_nodes)):
            all_nodes[i-1].add_child(all_nodes[i])
    else:
        # There are rollback points, build branch tree structure
        current_parent = root
        branch_start = 1
        
        for rollback_point in rollback_operation_points:
            # Find position of rollback point in operation list
            rollback_idx = -1
            for i, node in enumerate(all_nodes):
                if node.execution_number == rollback_point:
                    rollback_idx = i
                    break
            
            if rollback_idx == -1:
                continue
            
            # Build branch from branch_start to rollback_idx
            branch_parent = current_parent
            for i in range(branch_start, rollback_idx + 1):
                if i < len(all_nodes):
                    branch_parent.add_child(all_nodes[i])
                    branch_parent = all_nodes[i]
            
            # Next branch starts from rollback_idx + 1, parent node is root
            branch_start = rollback_idx + 1
            current_parent = root
        
        # Handle last branch
        if branch_start < len(all_nodes):
            branch_parent = current_parent
            for i in range(branch_start, len(all_nodes)):
                branch_parent.add_child(all_nodes[i])
                branch_parent = all_nodes[i]
    
    return root

def visualize_trace_tree(root, prefix="", is_last=True):
    """Visualize the operation relationship tree
    
    Args:
        root: Root node of the tree
        prefix: Prefix string for indentation
        is_last: Whether it's the last child of the parent node
    """
    if not root:
        return
        
    # Generate connection line for the current node
    connector = "└── " if is_last else "├── "
    
    # Print current node
    print(prefix + connector + f"{root.type}")
    
    # Print operation details
    detail_prefix = prefix + ("    " if is_last else "│   ")
    
    # Collect modified functions and line numbers
    if root.type == 'code_modification':
        modified_functions = set()
        line_numbers = []
        current_file = None
        
        for op in root.operations:
            if op['tool'] == 'str_replace_editor' and op['args']['command'] == 'str_replace':
                # Extract function name
                func_pattern = re.compile(r'def\s+(\w+)')
                matches = func_pattern.findall(op['args']['old_str'])
                if matches:
                    modified_functions.update(matches)
                
                # Extract line number information from file path
                if current_file != op['args']['path']:
                    current_file = op['args']['path']
                    # Assuming each file modification has corresponding line numbers
                    # Here we need to extract line number information from actual git patch
                    # Using a placeholder line number for now
                    line_numbers.append((476, 476))  # This should be replaced with actual line numbers
        
        if modified_functions:
            print(detail_prefix + f"Modified functions: {modified_functions}")
        if line_numbers:
            print(detail_prefix + f"Modified line number range: {line_numbers}")
    
    # Print other operation details
    for op in root.operations:
        if op['tool'] == 'execute_bash':
            print(detail_prefix + f"- Execute: {op['args']['command']}")
        elif op['tool'] == 'str_replace_editor':
            if op['args']['command'] == 'view':
                print(detail_prefix + f"- View: {op['args']['path']}")
            elif op['args']['command'] == 'str_replace':
                print(detail_prefix + f"- Modify: {op['args']['path']}")
                if root.is_alternative:
                    print(detail_prefix + "  (Alternative modification)")
    
    # Recursively process child nodes
    for i, child in enumerate(root.children):
        visualize_trace_tree(child, prefix + ("    " if is_last else "│   "), i == len(root.children) - 1)

def analyze_trace(base_dir, execution_results=None, execution_summary=None):
    """Analyze the agent's operation trajectory
    
    Args:
        base_dir: Directory containing all JSON conversation files
        execution_results: List of execution results (if None, will call analyze_trace_execution_result to get)
        execution_summary: Execution summary information (if None, will call analyze_trace_execution_result to get)
        
    Returns:
        str: Analysis result text
    """
    def count_rollbacks(traces, execution_results=None):
        """
        Calculate rollback count, based on the following logic:
        1. code_modification followed directly by code_analysis -> rollback
        2. test_execution failure followed by code_analysis -> rollback
        However: if code_modification is followed by test_execution, subsequent code_analysis should be based on test_execution result
        """
        rollback_count = 0
        last_modification_index = -1
        last_failed_test_index = -1
        
        # Create execution result mapping
        execution_map = {}
        if execution_results:
            for result in execution_results:
                exec_num = result.get('execution_number')
                if exec_num:
                    execution_map[exec_num] = result
        
        for i, trace in enumerate(traces):
            if trace['purpose'] == 'code_modification':
                last_modification_index = i
                # Reset failed test execution index, as logic restarts after code_modification
                last_failed_test_index = -1
            elif trace['purpose'] == 'test_execution':
                # Check if test_execution failed
                is_failed = False
                for operation in trace['operations']:
                    exec_num = operation.get('execution_number')
                    if exec_num and exec_num in execution_map:
                        result = execution_map[exec_num]
                        if "❌" in result['status']:
                            is_failed = True
                            break
                
                if is_failed:
                    last_failed_test_index = i
                    # If test_execution failed, reset modification index, as subsequent code_analysis should be based on test_execution failure
                    last_modification_index = -1
                else:
                    # If test_execution succeeded, reset failed index and modification index
                    last_failed_test_index = -1
                    last_modification_index = -1
            # If code_analysis appears after previous modification, it indicates a rollback
            elif trace['purpose'] == 'code_analysis':
                if last_modification_index != -1:
                    rollback_count += 1
                    debug_print(f"Debug: Found rollback point - Trace {last_modification_index} (code_modification) -> Trace {i} (code_analysis)")
                    last_modification_index = -1  # Reset, to avoid counting multiple times
                # If code_analysis appears after previous failed test_execution, it also indicates a rollback
                if last_failed_test_index != -1:
                    rollback_count += 1
                    debug_print(f"Debug: Found rollback point - Trace {last_failed_test_index} (test_execution failure) -> Trace {i} (code_analysis)")
                    last_failed_test_index = -1  # Reset, to avoid counting multiple times

        return rollback_count

    output = []
    
    # If execution results are not provided, call analyze_trace_execution_result to get
    if execution_results is None or execution_summary is None:
        _, _, execution_results, _ = analyze_trace_execution_result(base_dir)
    
    # if execution_summary:
        # output.append("\n=== Agent Operation Trajectory ===")
    
    # Get all JSON files in the directory
    json_files = []
    for file in os.listdir(base_dir):
        if file.endswith('.json'):
            full_path = os.path.join(base_dir, file)
            created_time = os.path.getmtime(full_path)
            json_files.append((created_time, full_path))
    
    # Sort by time
    json_files.sort(key=lambda x: x[0])
    
    # New: Global execution index counter
    global_exec_counter = 1
    
    # Analyze trajectory
    traces = []
    current_trace = {
        'purpose': '',
        'operations': []
    }
    
    for _, json_file in enumerate(json_files):
        try:
            with open(json_file[1], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'response' in data and 'choices' in data['response']:
                for choice in data['response']['choices']:
                    # Some messages in conversation may not have tool_calls, or the field may be None,
                    # Direct traversal will result in TypeError: 'NoneType' object is not iterable.
                    if 'message' in choice:
                        message = choice['message']
                        tool_calls = message.get('tool_calls') or []  # Ensure it's iterable

                        # If tool_calls is not a list (in extreme cases it may be dict or str), convert it to an empty list
                        if not isinstance(tool_calls, list):
                            tool_calls = []

                        for tool_call in tool_calls:
                            operation = {
                                'tool': tool_call['function']['name'],
                                'args': json.loads(tool_call['function']['arguments'])
                            }
                            # Assign a globally unique execution index to each tool call
                            operation['execution_number'] = global_exec_counter
                            global_exec_counter += 1
                            
                            # Analyze purpose of operation
                            if operation['tool'] == 'execute_bash':
                                cmd = operation['args']['command']
                                if cmd.startswith('find'):
                                    if current_trace.get('purpose') != 'file_location':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'file_location', 'operations': []}
                                elif cmd.startswith('grep'):
                                    if current_trace.get('purpose') != 'code_analysis':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'code_analysis', 'operations': []}
                                elif cmd.startswith('python3'):
                                    if current_trace.get('purpose') != 'test_execution':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'test_execution', 'operations': []}
                            
                            elif operation['tool'] == 'str_replace_editor':
                                if operation['args']['command'] == 'view':
                                    if current_trace.get('purpose') != 'code_analysis':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'code_analysis', 'operations': []}
                                elif operation['args']['command'] == 'str_replace':
                                    if current_trace.get('purpose') != 'code_modification':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'code_modification', 'operations': []}
                            
                            elif operation['tool'] == 'finish':
                                if current_trace['operations']:
                                    traces.append(current_trace)
                                current_trace = {'purpose': 'task_completion', 'operations': []}
                            
                            current_trace['operations'].append(operation)
                            
        except Exception as e:
            output.append(f"Error processing file: {str(e)}")
    
    # Add last trace
    if current_trace['operations']:
        traces.append(current_trace)

    # Print analysis results, using each operation's own execution number
    for i, trace in enumerate(traces, 1):
        first_exec_num = trace['operations'][0]['execution_number'] if trace['operations'] else 'N/A'
        # if execution_summary:
        #     output.append(f"\nTrace {i}: {trace['purpose']}")
            
        #     output.append("Operation sequence:")
        #     for op in trace['operations']:
        #         exec_num = op.get('execution_number', '?')
        #         if op['tool'] == 'execute_bash':
        #             output.append(f"- Execute command [TOOL EXECUTION #{exec_num}]: {op['args']['command']}")
        #         elif op['tool'] == 'str_replace_editor':
        #             if op['args']['command'] == 'view':
        #                 output.append(f"- View file [TOOL EXECUTION #{exec_num}]: {op['args']['path']}")
        #             elif op['args']['command'] == 'str_replace':
        #                 output.append(f"- Modify file [TOOL EXECUTION #{exec_num}]: {op['args']['path']}")
        #         elif op['tool'] == 'finish':
        #             output.append(f"- Complete task [TOOL EXECUTION #{exec_num}]: {op['args']['message'][:100]}...")
                    
    # Build and visualize operation relationship tree - using provided execution results
    root = build_trace_tree(traces, execution_results)
    output.append("\n=== Agent Operation Tree ===")
    output.extend(visualize_trace_tree_to_list(root))
    
    rollback_count = count_rollbacks(traces, execution_results)
    # Use the provided execution summary
    return "\n".join(output)

def visualize_trace_tree_to_list(root, prefix="", is_last=True):
    """Visualize the operation tree and return a list of text lines
    
    Args:
        root: The root node of the tree
        prefix: Prefix string for indentation
        is_last: Whether it is the last child of the parent node
        
    Returns:
        list: A list of text lines representing the visualization
    """
    if not root:
        return []
        
    output = []
    # Generate the connector for the current node
    connector = "└── " if is_last else "├── "
    
    # Add the current node and its status and execution number
    node_text = f"{root.type}"
    if root.execution_number:
        node_text += f" [TOOL EXECUTION #{root.execution_number}]"
    if root.execution_status:
        # Use a more obvious status symbol
        status_symbol = "✅ Success" if "✅" in root.execution_status else "❌ Failed"
        node_text += f" [{status_symbol}]"
    if root.tool_name:
        node_text += f" (Tool: {root.tool_name})"
    output.append(prefix + connector + node_text)
    
    # Print operation details
    detail_prefix = prefix + ("    " if is_last else "│   ")
    
    # First, show the specific execution command (most important information)
    for op in root.operations:
        if op['tool'] == 'execute_bash':
            command = op.get('args', {}).get('command', 'Unknown command')
            output.append(detail_prefix + f"🔧 Execute command: {command}")
        elif op['tool'] == 'str_replace_editor':
            args = op.get('args', {})
            if args.get('command') == 'view':
                file_path = args.get('path', 'Unknown file')
                output.append(detail_prefix + f"👀 View file: {file_path}")
                if 'view_range' in args:
                    view_range = args['view_range']
                    output.append(detail_prefix + f"   📍 Line range: {view_range}")
            elif args.get('command') == 'str_replace':
                file_path = args.get('path', 'Unknown file')
                output.append(detail_prefix + f"✏️  Modify file: {file_path}")
            elif args.get('command') == 'create':
                file_path = args.get('path', 'Unknown file')
                output.append(detail_prefix + f"📝 Create file: {file_path}")
            elif not args:
                # Handle cases without args, possibly a tool execution response
                output.append(detail_prefix + f"✏️  File edit operation (details not recorded)")
        elif op['tool'] == 'finish':
            message = op.get('args', {}).get('message', 'Task completed')
            message = message[:80] + "..." if len(message) > 80 else message
            output.append(detail_prefix + f"🎯 Complete task: {message}")
        else:
            # Handle other unknown tool types
            tool_name = op.get('tool', 'Unknown tool')
            output.append(detail_prefix + f"🔧 Tool execution: {tool_name}")
    
    # Then show error details (if any)
    if root.error_details:
        output.append(detail_prefix + "❗ Error details:")
        for error in root.error_details:
            if isinstance(error, dict):
                # If the error is in dictionary format, format it
                output.append(detail_prefix + f"   💥 {json.dumps(error, indent=2, ensure_ascii=False)}")
            elif isinstance(error, str):
                if error.startswith("  Error context:"):
                    # Error context in lighter color
                    output.append(detail_prefix + f"   {error}")
                elif error.startswith("- "):
                    # Main error information
                    error_type = error[2:].split(":")[0] if ":" in error else error[2:]
                    output.append(detail_prefix + f"   💥 {error[2:]}")
                else:
                    output.append(detail_prefix + f"   {error}")
            else:
                output.append(detail_prefix + f"   💥 {str(error)}")
    
    # For code modification operations, show the full code change content
    if root.type == 'code_modification':
        modified_functions = set()
        line_numbers = []
        current_file = None
        
        for op in root.operations:
            args = op.get('args', {})
            if op['tool'] == 'str_replace_editor' and args.get('command') == 'str_replace':
                # Extract function names
                old_str = args.get('old_str', '')
                func_pattern = re.compile(r'def\s+(\w+)')
                matches = func_pattern.findall(old_str)
                if matches:
                    modified_functions.update(matches)
                
                file_path = args.get('path', '')
                if current_file != file_path:
                    current_file = file_path
                    line_numbers.append((476, 476))
        
        if modified_functions:
            output.append(detail_prefix + f"🔧 Modified functions: {', '.join(modified_functions)}")
        if line_numbers:
            line_ranges = [f"{start}-{end}" if start != end else str(start) for start, end in line_numbers]
            output.append(detail_prefix + f"📍 Modified line numbers: {', '.join(line_ranges)}")
    
    # For code modification operations, show the full code change content
    for op in root.operations:
        args = op.get('args', {})
        if op['tool'] == 'str_replace_editor' and args.get('command') == 'str_replace':
            old_str = args.get('old_str', '')
            new_str = args.get('new_str', '')
            
            if old_str and new_str:
                # Show a summary of the code changes
                old_lines = len(old_str.split('\n'))
                new_lines = len(new_str.split('\n'))
                
                output.append(detail_prefix + "📍 Modified line number: 476")
                output.append(detail_prefix + "   📝 Code change summary:")
                output.append(detail_prefix + f"   - Lines removed: {old_lines}")
                output.append(detail_prefix + f"   - Lines added: {new_lines}")
                
                # Show the old and new code in full, without omitting any content
                # Handle escape characters: convert \n to actual newlines, \t to spaces
                old_code = old_str.replace('\\n', '\n').replace('\\t', '    ')
                new_code = new_str.replace('\\n', '\n').replace('\\t', '    ')
                
                output.append(detail_prefix + "   🔴 Old code:")
                output.append(detail_prefix + "   ```python")
                # Display line by line, ensuring each line is fully displayed
                for line in old_code.split('\n'):
                    # Maintain original indentation, make no changes
                    output.append(detail_prefix + "   " + line)
                output.append(detail_prefix + "   ```")
                
                output.append(detail_prefix + "   🟢 New code:")
                output.append(detail_prefix + "   ```python")
                for line in new_code.split('\n'):
                    # Maintain original indentation, make no changes
                    output.append(detail_prefix + "   " + line)
                output.append(detail_prefix + "   ```")
                    
                if root.is_alternative:
                    output.append(detail_prefix + "   ⚠️  (Alternative modification)")
            else:
                # If there is no old_str and new_str, show general information
                output.append(detail_prefix + "   📝 File edit operation executed")
    
    # Add a blank line to separate different nodes (improve readability)
    if root.children:
        output.append("")
    
    # Recursively process child nodes
    for i, child in enumerate(root.children):
        child_output = visualize_trace_tree_to_list(child, prefix + ("    " if is_last else "│   "), i == len(root.children) - 1)
        output.extend(child_output)
        
        # Add a separator line between child nodes (except the last one)
        if i < len(root.children) - 1:
            output.append("")
    
    return output

def analyze_patch_differences(generated_patch, ground_truth_patch):
    """Analyze differences between generated patch and ground truth patch
    
    Returns:
        tuple: (analysis result text, dictionary of statistics)
    """
    output = []
    
    def normalize_file_path(file_path):
        """Standardize file path, ensuring different formats of paths are recognized as the same file"""
        if not file_path:
            return file_path
            
        # Remove common prefixes
        prefixes_to_remove = [
            '/workspace/',
            'a/',
            'b/'
        ]
        
        # Dynamically recognize project-specific prefixes (e.g., project__project__version/ format)
        project_prefix_pattern = r'^[^/]+__[^/]+__[^/]+/'
        
        normalized = file_path
        
        # First remove other common prefixes
        for prefix in prefixes_to_remove:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
        
        # Then remove project-specific prefixes
        if re.match(project_prefix_pattern, normalized):
            normalized = re.sub(project_prefix_pattern, '', normalized)
        
        return normalized
    
    def extract_file_and_function_changes(patch):
        """Extract file and function modification information from patch"""
        changes = {}
        current_file = None
        
        if not patch:
            return changes
        
        lines = patch.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Identify file path
            if line.startswith('diff --git') or line.startswith('---') or line.startswith('+++'):
                # Extract file path from multiple formats
                if line.startswith('diff --git'):
                    # diff --git a/file b/file format
                    parts = line.split()
                    if len(parts) >= 4:
                        current_file = normalize_file_path(parts[-1])
                elif line.startswith('---'):
                    # --- a/file or --- /workspace/path/file format
                    file_path = line[4:].strip()
                    current_file = normalize_file_path(file_path)
                elif line.startswith('+++'):
                    # +++ b/file format, usually used to confirm file path
                    file_path = line[4:].strip()
                    current_file = normalize_file_path(file_path)
                
                if current_file and current_file not in changes:
                    changes[current_file] = {
                        'functions': set(),
                        'classes': set(),
                        'imports': {
                            'added': set(),
                            'removed': set()
                        },
                        'modified_lines': [],
                        'line_numbers': [],
                        'has_direct_function_def': False  # New: mark whether there's a direct function definition
                    }
            
            elif line.startswith('@@') and current_file:
                # Parse line number information
                line_info = re.findall(r'@@ -(\d+),?\d* \+(\d+),?\d* @@', line)
                if line_info:
                    old_start = int(line_info[0][0])
                    new_start = int(line_info[0][1])
                    changes[current_file]['line_numbers'].append((old_start, new_start))
            
            elif current_file and current_file in changes:
                # Analyze modified content
                if line.startswith(('+', '-', ' ')):
                    # Check if function definition or function call is included
                    clean_line = line[1:].strip() if line.startswith(('+', '-')) else line.strip()
                    
                    # 1. Direct function definition (highest priority)
                    func_def_match = re.search(r'def\s+(\w+)\s*\(', clean_line)
                    if func_def_match:
                        changes[current_file]['functions'].add(func_def_match.group(1))
                        changes[current_file]['has_direct_function_def'] = True
                    
                    # 3. Class definition
                    class_match = re.search(r'class\s+(\w+)', clean_line)
                    if class_match:
                        changes[current_file]['classes'].add(class_match.group(1))
                    
                    # 4. Import statement
                    if line.startswith('+'):
                        import_match = re.search(r'^(from\s+[\w.]+\s+import\s+.*|import\s+.*)', clean_line)
                        if import_match:
                            changes[current_file]['imports']['added'].add(import_match.group(1))
                    elif line.startswith('-'):
                        import_match = re.search(r'^(from\s+[\w.]+\s+import\s+.*|import\s+.*)', clean_line)
                        if import_match:
                            changes[current_file]['imports']['removed'].add(import_match.group(1))
                    
                    # Record modified lines
                    if line.startswith(('+', '-')):
                        changes[current_file]['modified_lines'].append(line)
            
            i += 1
        
        # Post-processing: only add functions if there's no direct function definition
        for file_path, file_changes in changes.items():
            if not file_changes['has_direct_function_def'] and file_changes['modified_lines']:
                # Infer possible function modifications based on keywords in modified content
                # This is a generic inference logic based on common keywords related to functions
                function_keywords = ['wrapper', 'bound_method', 'partial', 'wraps', 'decorator']
                
                for line in file_changes['modified_lines']:
                    line_content = line.lower()
                    for keyword in function_keywords:
                        if keyword in line_content:
                            # Infer function name based on file name and keyword
                            if 'decorators.py' in file_path and 'wrapper' in line_content:
                                file_changes['functions'].add('_wrapper')
                            elif 'bound_method' in line_content:
                                file_changes['functions'].add('bound_method')
                            break
                    if file_changes['functions']:  # If a function has been found, exit outer loop
                        break
                
            # Clean up temporary markers
            if 'has_direct_function_def' in file_changes:
                del file_changes['has_direct_function_def']
                
        return changes

    # Extract changes from both patches
    generated_changes = extract_file_and_function_changes(generated_patch) if generated_patch else {}
    ground_truth_changes = extract_file_and_function_changes(ground_truth_patch) if ground_truth_patch else {}
    
    # Calculate statistics
    generated_files = set(generated_changes.keys())
    ground_truth_files = set(ground_truth_changes.keys())
    common_files = generated_files & ground_truth_files
    
    # Calculate number of matching files and functions
    matched_files_count = len(common_files)
    matched_functions_count = 0
    
    for file in common_files:
        gen_funcs = generated_changes[file]['functions']
        gt_funcs = ground_truth_changes[file]['functions']
        matched_functions_count += len(gen_funcs & gt_funcs)
    
    stats = {
        'generated_files_count': len(generated_changes),
        'ground_truth_files_count': len(ground_truth_changes),
        'generated_functions_count': sum(len(changes['functions']) for changes in generated_changes.values()),
        'ground_truth_functions_count': sum(len(changes['functions']) for changes in ground_truth_changes.values()),
        'matched_files_count': matched_files_count,
        'matched_functions_count': matched_functions_count
    }
    
    # output.append("\n=== Detailed Patch Difference Analysis ===")
    
    # output.append("\n2. Comparison of Function, Class, and Import Modifications:")
    
    # First handle files modified in both patches
    # for file in common_files:
    #     output.append(f"\nFile: {file} (Modified in both patches)")
        
    #     # Print function modifications
    #     gen_funcs = generated_changes[file]['functions']
    #     gt_funcs = ground_truth_changes[file]['functions']
        
    #     output.append("Modified functions:")
    #     output.append(f"Generated patch: {gen_funcs}")
    #     output.append(f"Ground truth: {gt_funcs}")
        
    #     common_funcs = gen_funcs & gt_funcs
    #     if common_funcs:
    #         output.append(f"Commonly modified functions: {common_funcs}")
        
    #     if gen_funcs != gt_funcs:
    #         output.append("Function modification range mismatch:")
    #         only_in_gen = gen_funcs - gt_funcs
    #         only_in_gt = gt_funcs - gen_funcs
    #         if only_in_gen:
    #             output.append(f"Only modified in generated patch: {only_in_gen}")
    #         if only_in_gt:
    #             output.append(f"Only modified in ground truth: {only_in_gt}")
        
    #     # Print class modifications
    #     gen_classes = generated_changes[file]['classes']
    #     gt_classes = ground_truth_changes[file]['classes']
        
    #     if gen_classes or gt_classes:
    #         output.append("\nModified classes:")
    #         output.append(f"Generated patch: {gen_classes}")
    #         output.append(f"Ground truth: {gt_classes}")
        
    #     # Print import modifications
    #     output.append("\nImport statement modifications:")
    #     output.append("Generated patch:")
    #     output.append(f"  Added: {generated_changes[file]['imports']['added']}")
    #     output.append(f"  Removed: {generated_changes[file]['imports']['removed']}")
    #     output.append("Ground truth:")
    #     output.append(f"  Added: {ground_truth_changes[file]['imports']['added']}")
    #     output.append(f"  Removed: {ground_truth_changes[file]['imports']['removed']}")
        
    #     # Compare import differences
    #     added_imports_diff = generated_changes[file]['imports']['added'] ^ ground_truth_changes[file]['imports']['added']
    #     removed_imports_diff = generated_changes[file]['imports']['removed'] ^ ground_truth_changes[file]['imports']['removed']
        
    #     if added_imports_diff or removed_imports_diff:
    #         output.append("\nImport modification mismatch:")
    #         if added_imports_diff:
    #             output.append(f"  Added import mismatch: {added_imports_diff}")
    #         if removed_imports_diff:
    #             output.append(f"  Removed import mismatch: {removed_imports_diff}")
        
    #     output.append("\nModified line ranges:")
    #     output.append(f"Generated patch: {generated_changes[file]['line_numbers']}")
    #     output.append(f"Ground truth: {ground_truth_changes[file]['line_numbers']}")
    
    # Handle files only modified in the generated patch
    # only_in_generated = generated_files - ground_truth_files
    # if only_in_generated:
    #     for file in only_in_generated:
    #         output.append(f"\nFile: {file}")
    #         output.append("File only modified in generated patch")
    #         output.append(f"Modified functions: {generated_changes[file]['functions']}")
    #         output.append(f"Modified classes: {generated_changes[file]['classes']}")
    #         output.append(f"Modified line ranges: {generated_changes[file]['line_numbers']}")
    
    # # Handle files only modified in the ground truth
    # only_in_ground_truth = ground_truth_files - generated_files
    # if only_in_ground_truth:
    #     for file in only_in_ground_truth:
    #         output.append(f"\nFile: {file}")
    #         output.append("File only modified in ground truth")
    #         output.append(f"Modified functions: {ground_truth_changes[file]['functions']}")
    #         output.append(f"Modified classes: {ground_truth_changes[file]['classes']}")
    #         output.append(f"Modified line ranges: {ground_truth_changes[file]['line_numbers']}")
    
    return "\n".join(output), stats

def analyze_operation_tree(traces, execution_results=None):
    """Analyze the Agent's operation relationship tree
    
    Args:
        traces: List of traces, each containing purpose and operations
        execution_results: List of execution results
        
    Returns:
        dict: Dictionary containing various statistics
    """
    
    # Create execution result mapping
    execution_map = {}
    if execution_results:
        for result in execution_results:
            execution_map[result['execution_number']] = result
    
    # Expand all operations, each operation as a node
    operations = []
    for trace in traces:
        for operation in trace['operations']:
            exec_num = operation.get('execution_number')
            
            # Get execution status
            status = "✅ Success"  # Default success
            if exec_num and exec_num in execution_map:
                result = execution_map[exec_num]
                status = result['status']
            
            # Extract file information of the operation
            file_path = None
            if 'args' in operation:
                args = operation['args']
                if 'path' in args:
                    file_path = args['path']
                elif 'command' in args:
                    # Extract file path from command (if any)
                    cmd = args['command']
                    if 'python3' in cmd and '.py' in cmd:
                        # Extract Python file path
                        import re
                        match = re.search(r'(\S+\.py)', cmd)
                        if match:
                            file_path = match.group(1)
            
            operations.append({
                'type': trace['purpose'],
                'tool': operation['tool'],
                'execution_number': exec_num,
                'status': status,
                'is_failed': "❌" in status,
                'file_path': file_path
            })
    
    # Sort by execution index
    operations.sort(key=lambda x: x['execution_number'] if x['execution_number'] else 0)
    
    debug_print(f"Debug: Starting analysis of failure repair sequence")
    for i, op in enumerate(operations):
        debug_print(f"Debug: Operation {op['execution_number']}: {op['type']}, File: {op['file_path']}, Failed: {op['is_failed']}")
    
    # First determine the boundary of the operation subtree (based on rollback points)
    # Here we need to get rollback point information first
    rollback_points = []
    last_modification_index = -1
    last_failed_test_index = -1
    
    for i, op in enumerate(operations):
        if op['type'] == 'code_modification':
            last_modification_index = i
            last_failed_test_index = -1
        elif op['type'] == 'test_execution':
            if op['is_failed']:
                last_failed_test_index = i
                last_modification_index = -1
            else:
                last_failed_test_index = -1
                last_modification_index = -1
        elif op['type'] == 'code_analysis':
            if last_modification_index != -1:
                rollback_points.append(last_modification_index)
                last_modification_index = -1
            if last_failed_test_index != -1:
                rollback_points.append(last_failed_test_index)
                last_failed_test_index = -1
    
    debug_print(f"Debug: Operation index for rollback points: {rollback_points}")
    
    # Divide the tree based on rollback points
    subtrees = []
    start_idx = 0
    
    for rollback_point in sorted(rollback_points):
        if rollback_point >= start_idx:
            subtrees.append((start_idx, rollback_point))
            start_idx = rollback_point + 1
    
    # Add last subtree
    if start_idx < len(operations):
        subtrees.append((start_idx, len(operations) - 1))
    
    debug_print(f"Debug: Subtree division based on rollback points: {subtrees}")
    
    # New global logic for failure repair statistics
    # Collect all failed operations, grouped by (operation type, file)
    global_failure_stats = {}
    
    for i, op in enumerate(operations):
        if op['is_failed']:
            key = (op['type'], op['file_path'])
            if key not in global_failure_stats:
                global_failure_stats[key] = {
                    'failures': [],  # Index of failed operations
                    'successes': []  # Index of successful operations
                }
            global_failure_stats[key]['failures'].append(i)
        else:
            # Even successful operations should be recorded for later checks
            key = (op['type'], op['file_path'])
            if key not in global_failure_stats:
                global_failure_stats[key] = {
                    'failures': [],
                    'successes': []
                }
            global_failure_stats[key]['successes'].append(i)
    
    debug_print(f"Debug: Global failure statistics: {global_failure_stats}")
    
    # Analyze failure repair for each (operation type, file) combination
    failure_repair_count = 0
    failure_not_repair_count = 0
    
    for key, stats in global_failure_stats.items():
        op_type, file_path = key
        failures = stats['failures']
        successes = stats['successes']
        
        if not failures:
            continue  # No failures, skip
        
        debug_print(f"Debug: Global analysis - {op_type}({file_path}): Failed {[operations[i]['execution_number'] for i in failures]}, Success {[operations[i]['execution_number'] for i in successes]}")
        
        # For each failed operation, check if there's a subsequent successful operation of the same type
        for failure_idx in failures:
            failure_exec_num = operations[failure_idx]['execution_number']
            
            # Check if there's a subsequent successful operation of the same type after the failed operation
            has_later_success = False
            for success_idx in successes:
                success_exec_num = operations[success_idx]['execution_number']
                if success_exec_num > failure_exec_num:
                    has_later_success = True
                    debug_print(f"Debug: Failed operation {failure_exec_num} repaired by operation {success_exec_num}")
                    break
            
            if has_later_success:
                failure_repair_count += 1
            else:
                failure_not_repair_count += 1
                debug_print(f"Debug: Failed operation {failure_exec_num} not repaired")

    debug_print(f"Debug: Total number of failed repairs: {failure_repair_count}")
    debug_print(f"Debug: Total number of unrepaired failures: {failure_not_repair_count}")

    # 2. Count how many times test_execution occurs
    test_execution_count = len([op for op in operations if op['type'] == 'test_execution'])

    # 3, 4, 5. Analyze test_execution and code_modification relationship
    test_only_after_code_mod = 0  # Only after code_modification
    test_only_before_code_mod = 0  # Only before code_modification  
    test_between_code_mod = 0  # Both before and after code_modification
    test_without_code_mod = 0  # No code_modification tests

    # Find all positions of test_execution
    test_positions = []
    for i, op in enumerate(operations):
        if op['type'] == 'test_execution':
            test_positions.append(i)

    for pos in test_positions:
        # Check if there's a successful code_modification before the current position - traverse all previous operations, no restriction on type
        has_code_mod_before = False
        for j in range(pos - 1, -1, -1):
            if operations[j]['type'] == 'code_modification' and not operations[j]['is_failed']:
                has_code_mod_before = True
                break
        
        # Check if there's a successful code_modification after the current position - traverse all subsequent operations, no restriction on type
        has_code_mod_after = False
        for j in range(pos + 1, len(operations)):
            if operations[j]['type'] == 'code_modification' and not operations[j]['is_failed']:
                has_code_mod_after = True
                break

        # Classify based on code_modification before and after
        if has_code_mod_before and has_code_mod_after:
            test_between_code_mod += 1
        elif has_code_mod_before and not has_code_mod_after:
            test_only_after_code_mod += 1
        elif not has_code_mod_before and has_code_mod_after:
            test_only_before_code_mod += 1
        # If there's no code_modification before or after, this situation is not counted in any category
        else:
            test_without_code_mod += 1

    # 6. Check if the last test_execution was successful
    last_test_execution_success = None
    if test_execution_count > 0:
        # Find the last test_execution operation
        last_test_pos = -1
        for i in range(len(operations) - 1, -1, -1):
            if operations[i]['type'] == 'test_execution':
                last_test_pos = i
                break
        
        if last_test_pos >= 0:
            last_test_execution_success = not operations[last_test_pos]['is_failed']
   

    return {
        'failure_repair_count': failure_repair_count,
        'failure_not_repair_count': failure_not_repair_count,
        'test_execution_count': test_execution_count,
        'test_only_after_code_mod': test_only_after_code_mod,
        'test_only_before_code_mod': test_only_before_code_mod,
        'test_between_code_mod': test_between_code_mod,
        'test_without_code_mod': test_without_code_mod,
        'last_test_execution_success': last_test_execution_success
    }

def extract_key_metrics(output_jsonl_path, instance_id):
    """Extract key metrics from output.jsonl file"""
    metrics = {
        'generated_patch': None,
        'ground_truth_patch': None,
        'total_cost': 0.0,
        'total_rounds': 0
    }
    
    try:
        if not os.path.exists(output_jsonl_path):
            print(f"Warning: {output_jsonl_path} file does not exist")
            return metrics
            
        with open(output_jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    data = json.loads(line)
                    
                    # Check if it's the instance we're looking for
                    if data.get('instance', {}).get('instance_id') == instance_id:
                        # Extract total_cost
                        if 'metrics' in data and 'accumulated_cost' in data['metrics']:
                            metrics['total_cost'] = data['metrics']['accumulated_cost']
                        
                        # Extract total_rounds (length of history)
                        if 'history' in data:
                            metrics['total_rounds'] = len(data['history'])
                        
                        # Extract generated_patch (from the last successful edit action)
                        if 'history' in data:
                            for action in reversed(data['history']):
                                if action.get('observation') == 'edit':
                                    if 'extras' in action and 'diff' in action['extras']:
                                        diff_content = action['extras']['diff']
                                        if diff_content and diff_content.strip():
                                            metrics['generated_patch'] = diff_content
                                            break
                        
                        # Extract ground_truth_patch
                        if 'instance' in data and 'patch' in data['instance']:
                            metrics['ground_truth_patch'] = data['instance']['patch']
                        
                        break  # Exit after finding matching instance
                        
                except json.JSONDecodeError as e:
                    print(f"Warning: Error parsing JSON line: {e}")
                    continue
                    
    except Exception as e:
        print(f"Error: Error reading {output_jsonl_path}: {e}")
    
    return metrics

def collect_metrics_to_csv(base_dir, instance_id, output_jsonl_path, csv_path=None, write_to_file=True):
    """Collect key metrics to CSV file"""
    llm_completions_dir = os.path.join(base_dir, 'llm_completions', instance_id)

    if csv_path is None:
        csv_path = os.path.join(base_dir, 'metrics_summary.csv')
    
    # Collect execution results and trace analysis
    try:
        exec_dir, exec_file, execution_results, execution_summary = analyze_trace_execution_result(llm_completions_dir)
    except Exception as e:
        print(f"Error analyzing execution results: {str(e)}")
        execution_summary = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'success_rate': 0.0
        }
    
    # Collect key metrics
    try:
        metrics = extract_key_metrics(output_jsonl_path, instance_id)
    except Exception as e:
        print(f"Error extracting key metrics: {str(e)}")
        metrics = {
            'generated_patch': None,
            'ground_truth_patch': None,
            'total_cost': None,
            'total_rounds': None
        }
    
    # Analyze trajectory and get more statistics
    try:
        # Get trajectory statistics
        json_files = []
        for file in os.listdir(llm_completions_dir):
            if file.endswith('.json'):
                full_path = os.path.join(llm_completions_dir, file)
                created_time = os.path.getmtime(full_path)
                json_files.append((created_time, full_path))
        
        json_files.sort(key=lambda x: x[0])
        
        # Analyze trajectory
        traces = []
        current_trace = {'purpose': '', 'operations': []}
        # New: Global execution index counter
        global_exec_counter = 1
        
        for _, json_file in enumerate(json_files):
            try:
                with open(json_file[1], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if 'response' in data and 'choices' in data['response']:
                    for choice in data['response']['choices']:
                        message = choice['message']
                        tool_calls = message.get('tool_calls') or []
                        
                        if not isinstance(tool_calls, list):
                            tool_calls = []
                            
                        for tool_call in tool_calls:
                            operation = {
                                'tool': tool_call['function']['name'],
                                'args': json.loads(tool_call['function']['arguments'])
                            }
                            # Assign a globally unique execution index to each tool call
                            operation['execution_number'] = global_exec_counter
                            global_exec_counter += 1
                            
                            # Analyze purpose of operation
                            if operation['tool'] == 'execute_bash':
                                cmd = operation['args']['command']
                                if cmd.startswith('find'):
                                    if current_trace.get('purpose') != 'file_location':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'file_location', 'operations': []}
                                elif cmd.startswith('grep'):
                                    if current_trace.get('purpose') != 'code_analysis':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'code_analysis', 'operations': []}
                                elif cmd.startswith('python3'):
                                    if current_trace.get('purpose') != 'test_execution':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'test_execution', 'operations': []}
                            
                            elif operation['tool'] == 'str_replace_editor':
                                if operation['args']['command'] == 'view':
                                    if current_trace.get('purpose') != 'code_analysis':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'code_analysis', 'operations': []}
                                elif operation['args']['command'] == 'str_replace':
                                    if current_trace.get('purpose') != 'code_modification':
                                        if current_trace['operations']:
                                            traces.append(current_trace)
                                        current_trace = {'purpose': 'code_modification', 'operations': []}
                            
                            elif operation['tool'] == 'finish':
                                if current_trace['operations']:
                                    traces.append(current_trace)
                                current_trace = {'purpose': 'task_completion', 'operations': []}
                            
                            current_trace['operations'].append(operation)
                            
            except Exception as e:
                continue
        
        # Add last trace
        if current_trace['operations']:
            traces.append(current_trace)
        
        # Analyze trajectory
        modification_attempts = len([t for t in traces if t['purpose'] == 'code_modification'])
        has_test_execution = any(t['purpose'] == 'test_execution' for t in traces)
        task_completed = traces[-1]['purpose'] == 'task_completion' if traces else False
        
        # Redesign longest_path_length calculation logic, consistent with Agent Operation Tree
        # Analyze based on trace level rather than operation level, consistent with count_rollbacks logic
        
        # Expand all operations
        all_operations = []
        for trace in traces:
            for operation in trace['operations']:
                all_operations.append({
                    'execution_number': operation.get('execution_number'),
                    'type': trace['purpose'],
                    'tool': operation['tool']
                })
        
        # Sort by execution index
        all_operations.sort(key=lambda x: x['execution_number'] if x['execution_number'] else 0)
        
        debug_print(f"Debug: All operations: {[(op['execution_number'], op['type']) for op in all_operations]}")
        
        # Print information at trace level
        debug_print(f"Debug: Trace level information:")
        for i, trace in enumerate(traces):
            debug_print(f"  Trace {i}: {trace['purpose']}")
        
        # Use the same logic as count_rollbacks to identify rollback points
        # Based on trace level rather than operation level
        rollback_trace_indices = []
        last_modification_index = -1
        last_failed_test_index = -1
        
        # Create execution result mapping to determine if test_execution failed
        execution_map = {}
        if execution_results:
            for result in execution_results:
                execution_map[result['execution_number']] = result
        
        for i, trace in enumerate(traces):
            if trace['purpose'] == 'code_modification':
                last_modification_index = i
                # Reset failed test execution index, as logic restarts after code_modification
                last_failed_test_index = -1
            elif trace['purpose'] == 'test_execution':
                # Check if test_execution failed
                is_failed = False
                for operation in trace['operations']:
                    exec_num = operation.get('execution_number')
                    if exec_num and exec_num in execution_map:
                        result = execution_map[exec_num]
                        if "❌" in result['status']:
                            is_failed = True
                            break
                
                if is_failed:
                    last_failed_test_index = i
                    # If test_execution failed, reset modification index, as subsequent code_analysis should be based on test_execution failure
                    last_modification_index = -1
                else:
                    # If test_execution succeeded, reset failed index and modification index
                    last_failed_test_index = -1
                    last_modification_index = -1
            # If code_analysis appears after previous modification, it indicates a rollback
            elif trace['purpose'] == 'code_analysis':
                if last_modification_index != -1:
                    rollback_trace_indices.append(last_modification_index)
                    debug_print(f"Debug: Found rollback point - Trace {last_modification_index} (code_modification) -> Trace {i} (code_analysis)")
                    last_modification_index = -1  # Reset, to avoid counting multiple times
                # If code_analysis appears after previous failed test_execution, it also indicates a rollback
                if last_failed_test_index != -1:
                    rollback_trace_indices.append(last_failed_test_index)
                    debug_print(f"Debug: Found rollback point - Trace {last_failed_test_index} (test_execution failure) -> Trace {i} (code_analysis)")
                    last_failed_test_index = -1  # Reset, to avoid counting multiple times
        
        debug_print(f"Debug: Trace-level rollback indices: {rollback_trace_indices}")
        debug_print(f"Debug: Trace-level rollback count: {len(rollback_trace_indices)}")
        
        # Convert trace-level rollback points to operation-level split points
        # Find execution index of the last operation in each rollback trace
        rollback_operation_points = []
        for trace_idx in rollback_trace_indices:
            if trace_idx < len(traces) and traces[trace_idx]['operations']:
                # Get execution index of the last operation in the trace
                last_op_in_trace = traces[trace_idx]['operations'][-1]
                rollback_operation_points.append(last_op_in_trace['execution_number'])
        
        rollback_operation_points.sort()
        debug_print(f"Debug: Operation-level rollback split points: {rollback_operation_points}")
        
        # Calculate branch length
        if not rollback_operation_points:
            # No rollback points, the entire sequence is one branch
            longest_path_length = len(all_operations)
        else:
            branch_lengths = []
            start_exec = 1
            
            for rollback_point in rollback_operation_points:
                # Calculate length of branch from start_exec to rollback_point
                branch_length = rollback_point - start_exec + 1
                branch_lengths.append(branch_length)
                debug_print(f"Debug: Branch {start_exec}-{rollback_point} length: {branch_length}")
                start_exec = rollback_point + 1
            
            # Calculate last branch
            if start_exec <= len(all_operations):
                final_branch_length = len(all_operations) - start_exec + 1
                branch_lengths.append(final_branch_length)
                debug_print(f"Debug: Final branch {start_exec}-{len(all_operations)} length: {final_branch_length}")
            
            longest_path_length = max(branch_lengths)
        
        debug_print(f"Debug: Longest branch length: {longest_path_length}")
        
        # Get last operation type
        last_operation_type = traces[-1]['purpose'] if traces else 'unknown'
        
        # Count rollback count - using the same logic as count_rollbacks
        rollback_count = len(rollback_trace_indices)
        
        # Call new function for operation relationship tree analysis
        tree_analysis = analyze_operation_tree(traces, execution_results)
                
    except Exception as e:
        print(f"Error analyzing trajectory: {str(e)}")
        modification_attempts = 0
        has_test_execution = False
        task_completed = False
        rollback_count = 0
        longest_path_length = 0
        last_operation_type = 'unknown'
        # Set default values
        tree_analysis = {
            'failure_repair_count': 0,
            'failure_not_repair_count': 0,
            'test_execution_count': 0,
            'test_only_after_code_mod': 0,
            'test_only_before_code_mod': 0,
            'test_between_code_mod': 0,
            'test_without_code_mod': 0,
            'total_categorized_tests': 0,
            'categorization_complete': True,
            'last_test_execution_success': None
        }
    
    # Analyze patch differences and get statistics
    patch_stats = {
        'generated_files_count': 0,
        'ground_truth_files_count': 0,
        'generated_functions_count': 0,
        'ground_truth_functions_count': 0,
        'matched_files_count': 0,
        'matched_functions_count': 0
    }
    
    try:
        if metrics.get('generated_patch') or metrics.get('ground_truth_patch'):
            _, patch_stats = analyze_patch_differences(
                metrics.get('generated_patch'), 
                metrics.get('ground_truth_patch')
            )
    except Exception as e:
        print(f"Error analyzing patch differences: {str(e)}")
    
    # Build CSV row data
    csv_data = {
        'instance_id': instance_id,
        'total_cost': metrics.get('total_cost', 0),
        'total_rounds': metrics.get('total_rounds', 0),
        'total_executions': execution_summary.get('total_executions', 0),
        'longest_path_length': longest_path_length,
        'last_operation_type': last_operation_type,
        'successful_executions': execution_summary.get('successful_executions', 0),
        'failed_executions': execution_summary.get('failed_executions', 0),
        'failure_execution_repair_count': tree_analysis['failure_repair_count'],
        'failure_execution_not_repair_count': tree_analysis['failure_not_repair_count'],
        'success_rate': execution_summary.get('success_rate', 0.0),
        'modification_attempts': modification_attempts,
        'rollback_count': rollback_count,
        'has_generated_patch': metrics.get('generated_patch') is not None,
        'has_ground_truth_patch': metrics.get('ground_truth_patch') is not None,
        'generated_files_count': patch_stats['generated_files_count'],
        'ground_truth_files_count': patch_stats['ground_truth_files_count'],
        'generated_functions_count': patch_stats['generated_functions_count'],
        'ground_truth_functions_count': patch_stats['ground_truth_functions_count'],
        'matched_files_count': patch_stats['matched_files_count'],
        'matched_functions_count': patch_stats['matched_functions_count'],
        'test_execution_count': tree_analysis['test_execution_count'],
        'test_only_after_code_mod': tree_analysis['test_only_after_code_mod'],
        'test_only_before_code_mod': tree_analysis['test_only_before_code_mod'],
        'test_between_code_mod': tree_analysis['test_between_code_mod'],
        'test_without_code_mod': tree_analysis['test_without_code_mod'],
        'last_test_execution_success': tree_analysis['last_test_execution_success']
        # 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Only write to CSV file if write_to_file is True
    if write_to_file:
        # Check if CSV file exists, if not create and write header
        file_exists = os.path.exists(csv_path)
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'instance_id', 'total_cost', 'total_rounds', 'total_executions',
                'successful_executions', 'failed_executions', 'success_rate',
                'modification_attempts', 'rollback_count', 'longest_path_length', 
                'last_operation_type', 'has_generated_patch', 'has_ground_truth_patch',
                'generated_files_count', 'ground_truth_files_count', 'generated_functions_count', 
                'ground_truth_functions_count', 'matched_files_count', 'matched_functions_count',
                'failure_execution_repair_count', 'failure_execution_not_repair_count', 'test_execution_count',
                'test_only_after_code_mod', 'test_only_before_code_mod', 'test_between_code_mod',
                'test_without_code_mod', 'last_test_execution_success'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(csv_data)
        
        print(f"Metrics saved to CSV file: {csv_path}")
    
    return csv_data


def generate_analysis_report(base_dir, instance_id, output_jsonl_path, csv_data=None):
    """Generate analysis report"""
    llm_completions_dir = os.path.join(base_dir, 'llm_completions', instance_id)
    
    # If csv_data is not provided, collect metrics but do not write to file
    if csv_data is None:
        csv_data = collect_metrics_to_csv(base_dir, instance_id, output_jsonl_path, write_to_file=False)
    
    # Create output directory
    output_dir = os.path.join(llm_completions_dir, 'README')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate complete README file
    readme_path = os.path.join(output_dir, 'analysis_report_full.md')
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"# Analysis Report - {instance_id} Execution completed\n\n")
        
        # Write Agent Operation Tree
        exec_dir, exec_file, execution_results, execution_summary = analyze_trace_execution_result(llm_completions_dir)
        
        if execution_results and execution_summary:
            f.write("**Agent Operation Tree Description:** Hierarchical visualization of all agent operations showing the execution flow, tool usage, and operation relationships during the issue resolution process\n\n")
            tree_output = analyze_trace(llm_completions_dir, execution_results, execution_summary)
            f.write(tree_output)
            f.write("\n\n")


            # Add segment information below operation tree
            # f.write("## Operation Tree Analysis\n\n")
            # total_operations = len(execution_results)
            # failed_operations = len([res for res in execution_results if "❌" in res['status']])
            # success_operations = len([res for res in execution_results if "✅" in res['status']])
            
            # f.write(f"**Operation Tree Range:** Execution number 1 to {total_operations}\n")
            # f.write(f"**Total Operations:** {total_operations}\n")
            # f.write(f"**Rollback Count to Current Split Point:** {csv_data.get('rollback_count', 0)}\n")
            # f.write(f"**Failed Operations:** {failed_operations}\n")
            # f.write(f"**Successful Operations:** {success_operations}\n\n")
            
            # Add failure analysis
            if execution_results:
                # Analyze failure situation
                failure_stats = {}
                for result in execution_results:
                    exec_num = result['execution_number']
                    is_failed = "❌" in result['status']
                    
                    # Extract file path
                    file_path = None
                    if 'args' in result and isinstance(result.get('args'), dict):
                        file_path = result['args'].get('path')
                    elif hasattr(result, 'get') and 'content' in result:
                        # Try to extract file path from content
                        content = str(result['content'])
                        if '/workspace/' in content:
                            import re
                            match = re.search(r'/workspace/[^\s]+\.py', content)
                            if match:
                                file_path = match.group(0)
                    
                    # Use tool type as grouping key
                    tool_type = result.get('tool', 'unknown')
                    key = (tool_type, file_path)
                    if key not in failure_stats:
                        failure_stats[key] = {'failures': [], 'successes': []}
                    
                    if is_failed:
                        failure_stats[key]['failures'].append(exec_num)
                    else:
                        failure_stats[key]['successes'].append(exec_num)
                
                # Calculate failure situation
                repair_details = []
                for key, stats in failure_stats.items():
                    tool_type, file_path = key
                    failures = stats['failures']
                    successes = stats['successes']
                    
                    for failure_exec in failures:
                        repaired_by = None
                        for success_exec in successes:
                            if success_exec > failure_exec:
                                repaired_by = success_exec
                                break
                        
                        if repaired_by:
                            repair_details.append(f"Failed operation {failure_exec} repaired by operation {repaired_by}")
                        else:
                            repair_details.append(f"Failed operation {failure_exec} not repaired up to current execution")

                f.write("## Execution Summary\n\n")
                f.write("Comprehensive statistical overview of all operation executions, including success rates, failure counts, and detailed test execution pattern\n\n")
        
                # Write Failed Operations Repair Analysis
                if repair_details:
                    f.write("##Failed Operations Repair Analysis\n\n")
                    f.write("Analysis of failed operations and their subsequent repair attempts, tracking whether failed executions were resolved by later successful operations of the same type\n\n")
                    for detail in repair_details:
                        f.write(f"- {detail}\n")
                    f.write("\n")
        
        # Write Execution Summary
        f.write(f"**Total Executions:** {csv_data['total_executions']}\n")
        f.write(f"**Successful Executions:** {csv_data['successful_executions']}\n")
        f.write(f"**Failed Executions:** {csv_data['failed_executions']}\n")
        f.write(f"**Success Rate:** {csv_data['success_rate']:.2f}%\n")
        f.write(f" \n")
        f.write("Number of times the agent reverted to code analysis after unsuccessful code modifications or test executions\n")
        f.write(f"**Rollback Count:** {csv_data['rollback_count']}\n")
        f.write(f" \n")
        f.write("Number of the same type of task was executed after a failed step until success\n")
        f.write(f"**Failure Execution Repair Count:** {csv_data['failure_execution_repair_count']}\n")
        f.write(f"**Failure Execution Not Repaired Count:** {csv_data['failure_execution_not_repair_count']}\n")
        f.write(f" \n")
        f.write("Total number of test execution attempts during the debugging process\n")
        f.write(f"**Total Test Executions:** {csv_data['test_execution_count']}\n")
        f.write(f" \n")
        f.write("Test executions performed after code modifications to validate fixes, indicating tester verification behavior\n")
        f.write(f"**Tests Only After Code Modification:** {csv_data['test_only_after_code_mod']}\n")
        f.write(f" \n")
        f.write("Test executions performed before any code modifications, typically for issue reproduction and error identification behavior\n")
        f.write(f"**Tests Only Before Code Modification:** {csv_data['test_only_before_code_mod']}\n")
        f.write(f" \n")
        f.write("Test executions positioned between code modifications, indicating iterative debugging cycles with intermediate verification or reproduction, it depends on precious modification is for issue repair or test improvement\n")
        f.write(f"**Tests Between Code Modifications:** {csv_data['test_between_code_mod']}\n")
        f.write(f" \n")
        f.write("Test executions performed without any associated code modifications, for issue reproduction and error identification behavior\n")
        f.write(f"**Tests Without Code Modification:** {csv_data['test_without_code_mod']}\n")
        f.write(f" \n")
        f.write(f"Was the last test execution successful: {csv_data['last_test_execution_success']}\n\n")
           
        # Simplified verification statistics
        total_categorized = csv_data['test_only_after_code_mod'] + csv_data['test_only_before_code_mod'] + csv_data['test_between_code_mod'] + csv_data['test_without_code_mod']
        # if total_categorized == csv_data['test_execution_count']:
        #     f.write("✅ **Verification Passed:** Test execution classification statistics are correct\n")
        #     f.write(f"   - Number of categorized tests ({total_categorized}) = Total test executions ({csv_data['test_execution_count']})\n\n")
        # else:
        #     f.write("❌ **Verification Failed:** Test execution classification statistics do not match\n")
        #     f.write(f"   - Number of categorized tests: {total_categorized}\n")
        #     f.write(f"   - Total test executions: {csv_data['test_execution_count']}\n")
        #     f.write(f"   - Difference: {csv_data['test_execution_count'] - total_categorized}\n\n")
        
        # Get key metrics
        metrics = extract_key_metrics(output_jsonl_path, instance_id)
        
        # # Write Key Metrics section
        # f.write(f"\n## Key Metrics\n\n")
        
        if metrics['generated_patch']:
            f.write("**Generated Patch:**\n")
            f.write("```diff\n")
            f.write(metrics['generated_patch'])
            f.write("\n```\n\n")
        else:
            f.write("**Generated Patch:** Not found in data\n\n")
        
        # if metrics['ground_truth_patch']:
        #     f.write("**Ground Truth Patch:**\n")
        #     f.write("```diff\n")
        #     f.write(metrics['ground_truth_patch'])
        #     f.write("\n```\n\n")
        # else:
        #     f.write("**Ground Truth Patch:** Not found in data\n\n")
        
        f.write(f"**Total Cost:** {metrics['total_cost']}\n")
        f.write(f"**Total Rounds:** {metrics['total_rounds']}\n\n")
        
        # Patch difference analysis
        if metrics['generated_patch'] and metrics['ground_truth_patch']:
            diff_analysis, patch_stats = analyze_patch_differences(metrics['generated_patch'], metrics['ground_truth_patch'])
            f.write(diff_analysis)
            f.write("\n")
        elif metrics['generated_patch'] or metrics['ground_truth_patch']:
            _, patch_stats = analyze_patch_differences(metrics['generated_patch'], metrics['ground_truth_patch'])
            f.write(f"**Patch Statistics:**\n")
            f.write("**Patch Statistics Description:** Quantitative analysis of code modifications including the number of files and functions affected in the generated patch\n\n")
            f.write(f"- Number of files modified in Generated Patch: {patch_stats['generated_files_count']}\n")
            f.write(f"- Number of files modified in Ground Truth Patch: {patch_stats['ground_truth_files_count']}\n")
            f.write(f"- Number of functions modified in Generated Patch: {patch_stats['generated_functions_count']}\n")
            f.write(f"- Number of functions modified in Ground Truth Patch: {patch_stats['ground_truth_functions_count']}\n\n")
    
    print(f"Analysis report generated: {readme_path}")

def test_operation_tree_analysis(base_dir, instance_id, output_jsonl_path):
    """Test the operation tree analysis function"""
    
    print("Starting operation tree analysis test...")
    
    # Directly call the analysis function without writing to CSV
    csv_data = collect_metrics_to_csv(base_dir, instance_id, output_jsonl_path, write_to_file=False)
    
    # Output analysis results
    print(f"\n=== Operation Tree Analysis Results ===")
    print(f"Rollback Count: {csv_data['rollback_count']}")
    print("Rollback Count Description: Number of times the agent reverted to code analysis after unsuccessful code modifications or failed test executions")
    print(f"Failure Repair Count: {csv_data['failure_execution_repair_count']}")
    print("Failure Repair Count Description: Number of times the same type of task was executed after a failed step until success")
    print(f"Failure Not Repaired Count: {csv_data['failure_execution_not_repair_count']}")
    print("Failure Not Repaired Count Description: Total failed executions minus Failure Repair Count")
    print(f"Total Test Executions: {csv_data['test_execution_count']}")
    print("Total Test Executions Description: Total number of test execution attempts during the debugging process")
    print(f"Tests Only After Code Modification: {csv_data['test_only_after_code_mod']}")
    print("Tests Only After Code Modification Description: Test executions performed after code modifications to validate fixes, indicating verification behavior")
    print(f"Tests Only Before Code Modification: {csv_data['test_only_before_code_mod']}")
    print("Tests Only Before Code Modification Description: Test executions performed before any code modifications, typically for issue reproduction and error identification")
    print(f"Tests Between Code Modifications: {csv_data['test_between_code_mod']}")
    print("Tests Between Code Modifications Description: Test executions positioned between code modifications, indicating iterative debugging cycles with intermediate validation")
    print(f"Tests Without Code Modification: {csv_data['test_without_code_mod']}")
    print("Tests Without Code Modification Description: Test executions performed without any associated code modifications, often for exploration or verification purposes")
    print(f"Was the last test execution successful: {csv_data['last_test_execution_success']}")
        
    # Verify statistics correctness
    total_categorized = (csv_data['test_only_after_code_mod'] + 
                        csv_data['test_only_before_code_mod'] + 
                        csv_data['test_between_code_mod'] + 
                        csv_data['test_without_code_mod'])
 
    
    print(f"\n=== Statistics Verification ===")
    print(f"Total Categorized Tests: {total_categorized}")
    print(f"Total Test Executions: {csv_data['test_execution_count']}")
    print(f"Categorization Completeness: {'✓' if total_categorized == csv_data['test_execution_count'] else '✗'}")
    
    print("\nOperation tree analysis test completed!")

def main():
    # Turn off debug mode
    set_debug_mode(False)
    
    print("\n" + "="*50)
    print("Starting batch processing of all folders...")
    
    # Define all folders to be processed
    # folder_names = [
    #     "o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_both_removed_all",
    #     "o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_both_rephrased_all",
    #     "o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_both_reproduction_removed_all",
    #     "o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_both_reproduction_rephrased_all",
    #     "o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_both_runtime_error_removed_all",
    #     "o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_both_runtime_error_rephrased_all",
    #     "o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_og_all"
    # ]
    folder_names = [
        "claude-sonnet-4_maxiter_100_N_v0.48.0-no-hint-run_1_og",
    ]
    
    # Base path
    # base_path = "/Users/moonuke/Documents/Dataset/UQD/o3mini_res/CodeActAgent"
    base_path = "/Users/moonuke/Documents/Dataset/UQD/release/trajectories/claude4"
    
    # Total counter
    total_folders = len(folder_names)
    total_instances_processed = 0
    total_instances_failed = 0
    folder_results = []
    
    # Process each folder
    for folder_idx, folder_name in enumerate(folder_names, 1):
        print(f"\n{'='*70}")
        print(f"Processing folder {folder_idx}/{total_folders}: {folder_name}")
        print(f"{'='*70}")
        
        # Set current folder's path
        base_dir = os.path.join(base_path, folder_name)
        output_jsonl_path = os.path.join(base_dir, "output.jsonl")
        
        # Check if folder exists
        if not os.path.exists(base_dir):
            print(f"❌ Folder does not exist, skipping: {base_dir}")
            folder_results.append({
                'folder': folder_name,
                'status': 'folder_not_exist',
                'instances_processed': 0,
                'instances_failed': 0
            })
            continue
            
        # Check if output.jsonl file exists
        if not os.path.exists(output_jsonl_path):
            print(f"❌ output.jsonl file does not exist, skipping: {output_jsonl_path}")
            folder_results.append({
                'folder': folder_name,
                'status': 'output_jsonl_not_exist',
                'instances_processed': 0,
                'instances_failed': 0
            })
            continue
        
        # Read output_jsonl file to get all instance_id
        instance_ids = []
        try:
            with open(output_jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if 'instance' in data and 'instance_id' in data['instance']:
                            instance_id = data['instance']['instance_id']
                            if instance_id not in instance_ids:
                                instance_ids.append(instance_id)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"❌ Error reading output_jsonl file: {e}")
            folder_results.append({
                'folder': folder_name,
                'status': 'read_error',
                'instances_processed': 0,
                'instances_failed': 0
            })
            continue
        
        print(f"Found {len(instance_ids)} instances to process")
        
        # Process each instance one by one
        folder_processed_count = 0
        folder_failed_count = 0
        
        for i, instance_id in enumerate(instance_ids, 1):
            print(f"\n{'-'*50}")
            print(f"[{folder_name}] Processing instance {i}/{len(instance_ids)}: {instance_id}")
            print(f"{'-'*50}")
            
            try:
                # Check if directory exists for the instance
                instance_dir = os.path.join(base_dir, 'llm_completions', instance_id)
                if not os.path.exists(instance_dir):
                    print(f"Warning: Directory does not exist, skipping {instance_id}")
                    folder_failed_count += 1
                    continue
                
                # First run tests
                print(f"Testing operation tree analysis functionality - {instance_id}...")
                test_operation_tree_analysis(base_dir, instance_id, output_jsonl_path)
                
                # Collect metrics to CSV
                print(f"Collecting metrics to CSV - {instance_id}...")
                csv_data = collect_metrics_to_csv(base_dir, instance_id, output_jsonl_path)
                
                # Generate analysis report
                print(f"Generating analysis report - {instance_id}...")
                generate_analysis_report(base_dir, instance_id, output_jsonl_path, csv_data)

                # Generate segmented analysis reports
                generate_segmented_analysis_reports(base_dir, instance_id, output_jsonl_path, csv_data)
                
                folder_processed_count += 1
                print(f"✅ {instance_id} processed successfully")
                
            except Exception as e:
                print(f"❌ Error processing {instance_id}: {e}")
                folder_failed_count += 1
                continue
        
        # Record folder processing results
        folder_success_rate = (folder_processed_count / len(instance_ids) * 100) if len(instance_ids) > 0 else 0
        folder_results.append({
            'folder': folder_name,
            'status': 'completed',
            'total_instances': len(instance_ids),
            'instances_processed': folder_processed_count,
            'instances_failed': folder_failed_count,
            'success_rate': folder_success_rate
        })
        
        # Update total counter
        total_instances_processed += folder_processed_count
        total_instances_failed += folder_failed_count
        
        # Output folder processing summary
        print(f"\n{'='*50}")
        print(f"Folder {folder_name} processing completed!")
        print(f"Total number of instances: {len(instance_ids)}")
        print(f"Instances processed: {folder_processed_count}")
        print(f"Instances failed: {folder_failed_count}")
        print(f"Success rate: {folder_success_rate:.1f}%")
        print(f"{'='*50}")
    
    # Output final summary
    print(f"\n{'='*70}")
    print("🎉 All folders processed successfully!")
    print(f"{'='*70}")
    print(f"Total number of folders: {total_folders}")
    print(f"Total instances processed: {total_instances_processed}")
    print(f"Total instances failed: {total_instances_failed}")
    
    if total_instances_processed + total_instances_failed > 0:
        overall_success_rate = total_instances_processed / (total_instances_processed + total_instances_failed) * 100
        print(f"Overall success rate: {overall_success_rate:.1f}%")
    
    print(f"\n📊 Details of each folder processing:")
    for result in folder_results:
        if result['status'] == 'completed':
            print(f"✅ {result['folder']}: {result['instances_processed']}/{result['total_instances']} ({result['success_rate']:.1f}%)")
        elif result['status'] == 'folder_not_exist':
            print(f"❌ {result['folder']}: Folder does not exist")
        elif result['status'] == 'output_jsonl_not_exist':
            print(f"❌ {result['folder']}: output.jsonl file does not exist")
        elif result['status'] == 'read_error':
            print(f"❌ {result['folder']}: Error reading file")
    
    print(f"{'='*70}")

def test():
    set_debug_mode(True)
    base_dir = "/Users/moonuke/Documents/Dataset/UQD/o3mini_res/CodeActAgent/o3-mini_maxiter_100_N_v0.30.1-no-hint-run_1_both_removed_all"
    instance_id = "psf__requests-1724"
    output_jsonl_path = os.path.join(base_dir, "output.jsonl")
    
    # First run tests
    test_operation_tree_analysis(base_dir, instance_id, output_jsonl_path)
    # Only call collect_metrics_to_csv once, to collect key metrics to CSV
    csv_data = collect_metrics_to_csv(base_dir, instance_id, output_jsonl_path)
    # Generate analysis report, passing in collected csv_data
    generate_analysis_report(base_dir, instance_id, output_jsonl_path, csv_data)
    
    # Generate segmented analysis reports
    print("\n" + "="*50)
    print("Starting to generate segmented analysis reports...")
    print("="*50)
    segment_count = generate_segmented_analysis_reports(base_dir, instance_id, output_jsonl_path, csv_data)
    print(f"✅ {segment_count} segmented README files generated")
    print("="*50)

def generate_segmented_analysis_reports(base_dir, instance_id, output_jsonl_path, csv_data=None):
    """Generate multiple segmented README files based on rollback points"""
    llm_completions_dir = os.path.join(base_dir, 'llm_completions', instance_id)
    
    # If csv_data is not provided, collect metrics but do not write to file
    if csv_data is None:
        csv_data = collect_metrics_to_csv(base_dir, instance_id, output_jsonl_path, write_to_file=False)
    
    # Create output directory
    output_dir = os.path.join(llm_completions_dir, 'README')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get execution results and trace analysis
    exec_dir, exec_file, execution_results, execution_summary = analyze_trace_execution_result(llm_completions_dir)
    
    # Rebuild trajectory information to get rollback points
    json_files = []
    for file in os.listdir(llm_completions_dir):
        if file.endswith('.json'):
            full_path = os.path.join(llm_completions_dir, file)
            created_time = os.path.getmtime(full_path)
            json_files.append((created_time, full_path))
    
    json_files.sort(key=lambda x: x[0])
    
    # Analyze trajectory
    traces = []
    current_trace = {'purpose': '', 'operations': []}
    global_exec_counter = 1
    
    for _, json_file in enumerate(json_files):
        try:
            with open(json_file[1], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'response' in data and 'choices' in data['response']:
                for choice in data['response']['choices']:
                    message = choice['message']
                    tool_calls = message.get('tool_calls') or []
                    
                    if not isinstance(tool_calls, list):
                        tool_calls = []
                        
                    for tool_call in tool_calls:
                        operation = {
                            'tool': tool_call['function']['name'],
                            'args': json.loads(tool_call['function']['arguments'])
                        }
                        operation['execution_number'] = global_exec_counter
                        global_exec_counter += 1
                        
                        # Analyze purpose of operation
                        if operation['tool'] == 'execute_bash':
                            cmd = operation['args']['command']
                            if cmd.startswith('find'):
                                if current_trace.get('purpose') != 'file_location':
                                    if current_trace['operations']:
                                        traces.append(current_trace)
                                    current_trace = {'purpose': 'file_location', 'operations': []}
                            elif cmd.startswith('grep'):
                                if current_trace.get('purpose') != 'code_analysis':
                                    if current_trace['operations']:
                                        traces.append(current_trace)
                                    current_trace = {'purpose': 'code_analysis', 'operations': []}
                            elif cmd.startswith('python3'):
                                if current_trace.get('purpose') != 'test_execution':
                                    if current_trace['operations']:
                                        traces.append(current_trace)
                                    current_trace = {'purpose': 'test_execution', 'operations': []}
                        
                        elif operation['tool'] == 'str_replace_editor':
                            if operation['args']['command'] == 'view':
                                if current_trace.get('purpose') != 'code_analysis':
                                    if current_trace['operations']:
                                        traces.append(current_trace)
                                    current_trace = {'purpose': 'code_analysis', 'operations': []}
                            elif operation['args']['command'] == 'str_replace':
                                if current_trace.get('purpose') != 'code_modification':
                                    if current_trace['operations']:
                                        traces.append(current_trace)
                                    current_trace = {'purpose': 'code_modification', 'operations': []}
                        
                        elif operation['tool'] == 'finish':
                            if current_trace['operations']:
                                traces.append(current_trace)
                            current_trace = {'purpose': 'task_completion', 'operations': []}
                        
                        current_trace['operations'].append(operation)
                        
        except Exception as e:
            continue
    
    # Add the last trace
    if current_trace['operations']:
        traces.append(current_trace)
    
    # Expand all operations
    all_operations = []
    for trace in traces:
        for operation in trace['operations']:
            all_operations.append({
                'execution_number': operation.get('execution_number'),
                'type': trace['purpose'],
                'tool': operation['tool']
            })
    
    all_operations.sort(key=lambda x: x['execution_number'] if x['execution_number'] else 0)
    
    # Get rollback split points
    rollback_trace_indices = []
    last_modification_index = -1
    last_failed_test_index = -1
    
    execution_map = {}
    if execution_results:
        for result in execution_results:
            execution_map[result['execution_number']] = result
    
    for i, trace in enumerate(traces):
        if trace['purpose'] == 'code_modification':
            last_modification_index = i
            last_failed_test_index = -1
        elif trace['purpose'] == 'test_execution':
            is_failed = False
            for operation in trace['operations']:
                exec_num = operation.get('execution_number')
                if exec_num and exec_num in execution_map:
                    result = execution_map[exec_num]
                    if "❌" in result['status']:
                        is_failed = True
                        break
            
            if is_failed:
                last_failed_test_index = i
                last_modification_index = -1
            else:
                last_failed_test_index = -1
                last_modification_index = -1
        elif trace['purpose'] == 'code_analysis':
            if last_modification_index != -1:
                rollback_trace_indices.append(last_modification_index)
                last_modification_index = -1
            if last_failed_test_index != -1:
                rollback_trace_indices.append(last_failed_test_index)
                last_failed_test_index = -1
    
    # Convert to operation-level split points
    rollback_operation_points = []
    for trace_idx in rollback_trace_indices:
        if trace_idx < len(traces) and traces[trace_idx]['operations']:
            last_op_in_trace = traces[trace_idx]['operations'][-1]
            rollback_operation_points.append(last_op_in_trace['execution_number'])
    
    rollback_operation_points.sort()
    
    debug_print(f"Debug: Rollback split points: {rollback_operation_points}")
    
    # Generate README file for each split point
    segment_points = rollback_operation_points.copy()
    
    for i, split_point in enumerate(segment_points):
        debug_print(f"Debug: Generating segment {i+1} README")
        
        # Filter operations up to current split point
        segment_operations = [op for op in all_operations if op['execution_number'] <= split_point]
        segment_execution_results = [res for res in execution_results if res['execution_number'] <= split_point]
        
        # Rebuild traces for this segment
        segment_traces = []
        for trace in traces:
            segment_trace = {'purpose': trace['purpose'], 'operations': []}
            for operation in trace['operations']:
                if operation['execution_number'] <= split_point:
                    segment_trace['operations'].append(operation)
            if segment_trace['operations']:
                segment_traces.append(segment_trace)
        
        # Calculate statistics for this segment
        segment_rollback_count = i + 1  # Number of rollbacks up to current split point
        segment_failed_count = len([res for res in segment_execution_results if "❌" in res['status']])
        segment_success_count = len([res for res in segment_execution_results if "✅" in res['status']])
        
        # Analyze repair status for this segment
        segment_failure_stats = {}
        for j, op in enumerate(segment_operations):
            exec_num = op['execution_number']
            if exec_num in execution_map:
                result = execution_map[exec_num]
                is_failed = "❌" in result['status']
                
                # Extract file path
                file_path = None
                if 'args' in result and isinstance(result.get('args'), dict):
                    file_path = result['args'].get('path')
                elif hasattr(result, 'get') and 'content' in result:
                    # Try to extract file path from content
                    content = str(result['content'])
                    if '/workspace/' in content:
                        import re
                        match = re.search(r'/workspace/[^\s]+\.py', content)
                        if match:
                            file_path = match.group(0)
                
                key = (op['type'], file_path)
                if key not in segment_failure_stats:
                    segment_failure_stats[key] = {'failures': [], 'successes': []}
                
                if is_failed:
                    segment_failure_stats[key]['failures'].append(exec_num)
                else:
                    segment_failure_stats[key]['successes'].append(exec_num)
        
        # Calculate repair status
        segment_repair_details = []
        for key, stats in segment_failure_stats.items():
            op_type, file_path = key
            failures = stats['failures']
            successes = stats['successes']
            
            for failure_exec in failures:
                repaired_by = None
                for success_exec in successes:
                    if success_exec > failure_exec:
                        repaired_by = success_exec
                        break
                
                if repaired_by:
                    segment_repair_details.append(f"Failed operation {failure_exec} was repaired by operation {repaired_by}")
                else:
                    segment_repair_details.append(f"Failed operation {failure_exec} was not repaired up to current excurtion")
        
        # Generate README file
        readme_file = f'analysis_report_segment_{i+1}.md'
        readme_path = os.path.join(output_dir, readme_file)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# Analysis Report to Current Execution \n\n")
            
            # Generate operation tree for this segment
            segment_root = build_trace_tree(segment_traces, segment_execution_results)
            if segment_root:
                f.write("**Agent Operation Tree Description:** Hierarchical visualization of operations, showing the execution flow and tool usage up to the current execution\n\n")
                segment_tree_output = visualize_trace_tree_to_list(segment_root)
                for line in segment_tree_output:
                    f.write(line + "\n")
                f.write("\n")

                f.write("## Execution Summary\n\n")
                f.write("Comprehensive statistical overview of all operation executions within the current segment, including success rates, failure counts, and detailed test execution pattern\n\n")
            
                
                if segment_repair_details:
                    f.write("## Failed Operations Repair Analysis\n\n")
                    f.write("Analysis of failed operations and their subsequent repair attempts, tracking whether failed executions were resolved by later successful operations of the same type\n\n")
                    for detail in segment_repair_details:
                        f.write(f"- {detail}\n")
                    f.write("\n")

            # Add segment execution summary - Calculate detailed statistics for this segment
            segment_success_rate = (segment_success_count / len(segment_operations) * 100) if segment_operations else 0
            
            # Analyze operation tree for this segment to get detailed statistics
            segment_analysis = analyze_operation_tree(segment_traces, segment_execution_results)
            
            
            f.write(f"**Total Executions:** {len(segment_operations)}\n")
            f.write(f"**Successful Executions:** {segment_success_count}\n")
            f.write(f"**Failed Executions:** {segment_failed_count}\n")
            f.write(f"**Success Rate:** {segment_success_rate:.2f}%\n")
            f.write(f"**Rollback Count:** {segment_rollback_count}\n")
            f.write(f" \n")
            f.write("Number of times the agent reverted to code analysis after unsuccessful code modifications or failed test executions\n")
            f.write(f"**Failure Repair Count:** {segment_analysis['failure_repair_count']}\n")
            f.write(f" \n")
            f.write("Number of times the same type of task was executed after a failed step until success\n")
            f.write(f"**Failure Not Repaired Count:** {segment_analysis['failure_not_repair_count']}\n")
            f.write(f" \n")
            f.write("Total number of test execution attempts during the debugging process\n")
            f.write(f"**Total Test Executions:** {segment_analysis['test_execution_count']}\n")
            f.write(f" \n")
            f.write("Test executions performed after code modifications to validate fixes, indicating verification behavior\n")
            f.write(f"**Tests Only After Code Modification:** {segment_analysis['test_only_after_code_mod']}\n")
            f.write(f" \n")
            f.write("Test executions performed before any code modifications, typically for issue reproduction and error identification behavior\n")
            f.write(f"**Tests Only Before Code Modification:** {segment_analysis['test_only_before_code_mod']}\n")
            f.write(f" \n")
            f.write("Test executions positioned between code modifications, indicating iterative debugging cycles with intermediate validation\n")
            f.write(f"**Tests Between Code Modifications:** {segment_analysis['test_between_code_mod']}\n")
            f.write(f" \n")
            f.write("Test executions performed without any associated code modifications, often for exploration or verification purposes\n")
            f.write(f"**Tests Without Code Modification:** {segment_analysis['test_without_code_mod']}\n")
            f.write(f" \n")
            f.write(f"Was the last test execution successful: {segment_analysis['last_test_execution_success']}\n\n")
            

        print(f"Generated segmented README: {readme_path}")
    
    return len(segment_points)

if __name__ == "__main__":
    main()
    
    # test()