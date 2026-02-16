from google.genai import types
import os
osp = os.path
def write_file(working_directory, file_path, content):
    try:
        work_abs = osp.abspath(working_directory)
        file_dir = osp.normpath(osp.join(work_abs, file_path))

        if not osp.commonpath([work_abs, file_dir]) == work_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if osp.isdir(file_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    
        os.makedirs(file_path, exist_ok = True)

        with open(file_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"Error: {e}")

schema_write_file = types.FunctionDeclaration(
        name = "write_file",
        description = "Write to a file using the provided content in the provided file path",
        parameters = types.Schema(
            type = types.Type.OBJECT,
            properties = {
                "file_path": types.Schema(
                type = types.Type.STRING,
                description = "File path to the file",
                ),
                "content": types.Schema(
                type = types.Type.STRING,
                description = "Content to write in the file",
                ),
            },
        ),
    )
