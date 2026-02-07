import os
from config import MAX_CHARS
path = os.path
def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = path.abspath(working_directory)
        file_dir = path.normpath(path.join(working_dir_abs, file_path))
    
        if not path.commonpath([working_dir_abs, file_dir]) == working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not path.isfile(file_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(file_dir, "r") as f:
            file_content_str = f.read(MAX_CHARS)
            if f.read(1):
                file_content_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_str
    except Exception as e:
        print(f"Error: {e}")
