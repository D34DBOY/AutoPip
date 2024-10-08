import subprocess
import re
import sys
import logging
import os

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='install_log.log', filemode='a')

def install_missing_module(module_name):
    """Attempt to install a missing module using pip."""
    logging.info(f"Attempting to install missing module: {module_name}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        logging.info(f"Successfully installed module: {module_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install module: {module_name}. Error: {e}")

def run_script(file_name):
    """Run the selected Python script and check for missing modules."""
    python_executable = "python" if sys.platform.startswith("win") else "python3"
    result = subprocess.run([python_executable, file_name], capture_output=True, text=True)

    # Log standard output   ``
    logging.info(f"Script output:\n{result.stdout.strip()}")

    # Log standard errors
    if result.stderr:
        logging.error(f"Script error:\n{result.stderr.strip()}")

    # Check for ModuleNotFoundError and extract the missing module name
    module_not_found_pattern = r"ModuleNotFoundError: No module named ['\"](\w+)['\"]"
    match = re.search(module_not_found_pattern, result.stderr)

    return match

def list_python_files(directory):
    """Return a list of .py files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.py')]

def main():
    # Determine the project directory (current working directory)
    project_dir = os.getcwd()

    # Get a list of .py files in the project directory
    py_files = list_python_files(project_dir)

    if not py_files:
        print("No Python files found in the current directory.")
        logging.error("No Python files found in the current directory.")
        return

    print("Python files available in the current directory:")
    for i, file_name in enumerate(py_files, 1):
        print(f"{i}. {file_name}")

    # Prompt the user to select a Python file to execute
    try:
        choice = int(input("Please enter the number of the Python file you want to execute: "))
        if choice < 1 or choice > len(py_files):
            raise ValueError("Invalid choice")
        file_name = py_files[choice - 1]
    except (ValueError, IndexError) as e:
        print("Invalid input. Exiting.")
        logging.error(f"Invalid input. {e}")
        return

    print(f"Selected file: {file_name}")

    # Loop to continuously run the script until no missing modules are found
    while True:
        error_match = run_script(file_name)

        if error_match:
            missing_module = error_match.group(1)
            install_missing_module(missing_module)
        else:
            logging.info("All required modules are installed. No more errors.")
            print("All required modules are installed. No more errors.")
            break

if __name__ == "__main__":
    main()
