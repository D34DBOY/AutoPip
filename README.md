
# Python Dependency Auto-Installer Script

## Introduction

Since this is a simple script, I decided to use ChatGPT to help write it. There have been many times when I've forgotten to include the required dependencies for a project, and I wanted to save time by automating the installation process. I realized that such a tool could be helpful not only for me but also for others. I hope this script proves useful for you as well!

## Features

- **Automatic Module Installation**: Detects and installs missing Python modules required by your script.
- **Cross-Platform**: Compatible with both Windows and Linux, automatically determining whether to use `python` or `python3`.
- **Project-Wide Compatibility**: Lists all `.py` files in the project directory and allows the user to select one to execute.
- **Continuous Execution**: The script runs continuously until all dependencies are satisfied.
- **Detailed Logging**: All actions, including successful installations and any errors encountered, are logged in a file (`install_log.log`).

## How It Works

1. **Script Discovery**: The script identifies all `.py` files in the current project directory.
2. **User Selection**: The user is prompted to select a Python file from the list of discovered `.py` files to execute.
3. **Execution and Error Handling**: The script attempts to run the selected Python file. If it encounters a `ModuleNotFoundError`, it uses a regular expression to extract the name of the missing module.
4. **Installation**: The script then attempts to install the missing module using `pip`.
5. **Re-run**: After installation, the script re-runs the selected Python file. This process repeats until no more `ModuleNotFoundError` exceptions are encountered.
6. **Logging**: Every step, including successful runs, installation attempts, and errors, is logged in the `install_log.log` file.
7. **Completion**: Once all required modules are installed, the script notifies the user and stops.

## Script Overview

### Main Script

```python
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

    # Log standard output
    logging.info(f"Script output:\n{result.stdout.strip()}")

    # Log standard errors
    if result.stderr:
        logging.error(f"Script error:\n{result.stderr.strip()}")

    # Check for ModuleNotFoundError and extract the missing module name
    module_not_found_pattern = r"ModuleNotFoundError: No module named ['"](\w+)['"]"
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
```

### How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/python-dependency-installer.git
   cd python-dependency-installer
   ```

2. **Run the Script**:
   Execute the script using Python:
   ```bash
   python auto_installer.py
   ```
   - The script will display a list of all `.py` files in the current directory and prompt you to select one for execution.
   
3. **Monitor Logs**:
   - All actions and errors are logged in `install_log.log`. Review this file to monitor the script's progress and troubleshoot any issues.

### Example Usage

Suppose you have a project with multiple Python scripts, and one of them requires external libraries that are not yet installed. This script will:

1. List all `.py` files in the current directory.
2. Allow you to select the script you want to run.
3. Automatically detect and install any missing modules.
4. Re-run the script until all dependencies are satisfied.
5. Log all actions and errors for review.

### Customization

- **Logging**: Modify the logging configuration to suit your needs (e.g., change log file name, adjust log level).
- **Error Handling**: Extend error handling to cover more scenarios or customize the regular expressions for more precise module detection.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
