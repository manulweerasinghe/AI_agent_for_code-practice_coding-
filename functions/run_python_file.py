from google.genai import types
import os
import subprocess
osp = os.path
def run_python_file(working_directory, file_path, args = None):
    try:
        work_abs_dir = osp.abspath(working_directory)
        file_dir = osp.normpath(osp.join(work_abs_dir, file_path))
        if not osp.commonpath([work_abs_dir, file_dir]) == work_abs_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not osp.isfile(file_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
    
        command = ["python", file_dir]
        if args != None:
            command.extend(args)
    
        result = subprocess.run(command, capture_output = True, timeout = 30, text = True)
        exit_code = result.returncode
        output_str = ""
        if exit_code != 0:
            output_str = f"Process exited with code {exit_code}"
        if result.stdout == None or result.stderr == None:
            output_str += "No output produced"
        else:
                output_str += f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
        name = "run_python_file",
        description = "Runs python file using the provided file path with argumets that also gets provided",
        parameters = types.Schema(
            type = types.Type.OBJECT,
            properties = {
                "file_path": types.Schema(
                    type = types.Type.STRING,
                    description = "File path to run the file",
                    ),
                "args": types.Schema(
                    type = types.Type.ARRAY,
                    description = "Arguments needed to run the file (default is Python None type)",
                    items = types.Schema(
                        type = types.Type.STRING,
                        ),
                    ),
                },
            )
        )
