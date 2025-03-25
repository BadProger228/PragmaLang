import subprocess
import os

def compile_il(il_file_path):

    il_file_path += '.il'
    
    if not os.path.isfile(il_file_path):
        return f"Error: File '{il_file_path}' does not exist."
    
    if not il_file_path.endswith(".il"):
        return "Error: Input file must have a .il extension."

    il_directory = os.path.dirname(il_file_path) or "."
    il_file_name = os.path.basename(il_file_path)
    output_file = "solve" + ".exe"

    command = [
        "ilasm",
        il_file_name,
        f"/output={output_file}"
    ]

    try:
        print(f"Executing command: {' '.join(command)} in directory: {il_directory}")
        result = subprocess.run(
            command,
            cwd=il_directory,
            text=True,
            capture_output=True,
            check=True,
            shell=True
        )
        return os.path.join(il_directory, output_file)
    except Exception as e:
        return e



def run(exe_file):

    if "Error" in exe_file or isinstance(exe_file, Exception):
        return exe_file

    try:
        print(f"Running the program: {exe_file}")
        result = subprocess.run(
            [exe_file], 
            text=True, 
            capture_output=True, 
            check=True,
            shell=True
        )
        return f"Program output:\n{result.stdout}"
    except Exception as e:
        return f"Error running the program: {e}"
