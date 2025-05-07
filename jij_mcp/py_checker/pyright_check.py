import subprocess
import tempfile
import os
import sys
import re


# This is the core Pyright checking logic adapted from our previous conversation.
# It will be called by the main function to check code using a specific Pyright executable.
def _run_pyright_on_file(
    code_file_to_check: str, pyright_executable_in_venv: str
) -> dict:
    """
    Runs Pyright on a specified file using a specific Pyright executable.
    Parses the output to extract errors and determine success.
    File paths in the output are replaced with a placeholder.
    """
    check_result = {"success": False, "output": "", "errors": []}
    # Placeholder to display instead of temporary file paths
    # To use a fixed filename in feedback to AI
    file_placeholder = "[checked_code.py]"

    try:
        process = subprocess.run(
            [pyright_executable_in_venv, code_file_to_check],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        raw_output = process.stdout + process.stderr

        # Success/failure determination (based on Pyright's summary line)
        num_errors = -1
        summary_patterns = [
            re.compile(
                r"(\d+)\s*error[s]?,\s*(\d+)\s*warning[s]?,\s*(\d+)\s*information[s]?",
                re.IGNORECASE,
            ),
            re.compile(r"found\s*(\d+)\s*error[s]?", re.IGNORECASE),
            re.compile(r"no\s*error[s]?\s*found", re.IGNORECASE),
        ]

        for pattern in summary_patterns:
            match = pattern.search(raw_output)
            if match:
                if pattern.pattern == summary_patterns[0].pattern:
                    num_errors = int(match.group(1))
                    break
                elif pattern.pattern == summary_patterns[1].pattern:
                    num_errors = int(match.group(1))
                    break
                elif pattern.pattern == summary_patterns[2].pattern:
                    num_errors = 0
                    break

        if num_errors == 0:
            check_result["success"] = True
        elif num_errors > 0:
            check_result["success"] = False
        else:
            if process.returncode == 0 and not "error" in raw_output.lower():
                check_result["success"] = True
            elif process.returncode != 0:
                check_result["success"] = False
            else:
                check_result["success"] = False

        # Clean Pyright output by replacing the temporary file path
        cleaned_output_lines = []
        for line in raw_output.splitlines():
            cleaned_line = line.replace(code_file_to_check, file_placeholder)
            cleaned_output_lines.append(cleaned_line)
        check_result["output"] = "\n".join(cleaned_output_lines).strip()

        # Extract pure error messages
        parsed_errors = []
        for line in raw_output.splitlines():  # Parse from raw_output
            marker = " - error: "
            marker_index = line.lower().find(marker)
            if marker_index != -1:
                message_body = line[marker_index + len(marker) :].strip()
                message_body = re.sub(
                    r"\s*\([a-zA-Z0-9_-]+\)$",
                    "",
                    message_body,  # Remove trailing (ruleName)
                ).strip()
                parsed_errors.append(message_body)
            elif (
                ": error: " in line.lower() and code_file_to_check in line
            ):  # Handle other formats if they contain the specific file
                try:
                    _prefix_part, msg_body = line.split(" error: ", 1)
                    msg_body = re.sub(
                        r"\s*\([a-zA-Z0-9_-]+\)$", "", msg_body.strip()
                    ).strip()
                    parsed_errors.append(msg_body)
                except ValueError:
                    pass  # Could not split, ignore this line for error parsing
        check_result["errors"] = parsed_errors

    except FileNotFoundError:
        check_result["output"] = (
            f"Error: Pyright executable '{pyright_executable_in_venv}' not found."
        )
        check_result["errors"].append(
            f"Pyright executable '{pyright_executable_in_venv}' not found."
        )
        check_result["success"] = False
    except Exception as e:
        check_result["output"] = (
            f"An unexpected error occurred during Pyright check: {str(e)}"
        )
        check_result["errors"].append(f"An unexpected error: {str(e)}")
        check_result["success"] = False
    return check_result


def run_code_in_temporary_venv(
    ai_code_string: str,
    dependencies: list[str],
    execute_code_after_check: bool = True,  # Default to True to try execution
) -> dict:
    """
    Creates a temporary virtual environment, installs dependencies and Pyright,
    statically checks the AI-generated code with Pyright, and optionally executes the code.

    Args:
        ai_code_string: The Python code string to check and execute.
        dependencies: A list of Python package dependencies (e.g., ["requests", "numpy>=1.20"]).
        execute_code_after_check: If True, executes the code after a successful Pyright check.

    Returns:
        dict: A dictionary containing results from each step.
    """
    results = {
        "venv_path": None,
        "venv_created": False,
        "dependencies_installed": False,
        "pyright_check_result": None,
        "code_execution_result": {
            "executed": False,
            "success": None,
            "stdout": None,
            "stderr": None,
            "return_code": None,
        },
        "log": [],  # Overall log of operations
    }

    # Create a temporary directory that will be automatically cleaned up
    with tempfile.TemporaryDirectory(prefix="ai_code_venv_") as venv_dir:
        results["venv_path"] = venv_dir
        results["log"].append(f"Temporary venv directory created: {venv_dir}")

        # 1. Create the virtual environment
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", venv_dir],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            results["venv_created"] = True
            results["log"].append("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            results["log"].append(f"Venv creation failed: {e.stderr}")
            return results  # Critical failure, stop here

        # Determine paths to executables within the venv
        if sys.platform == "win32":
            pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
            python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
            pyright_exe = os.path.join(venv_dir, "Scripts", "pyright.exe")
        else:
            pip_exe = os.path.join(venv_dir, "bin", "pip")
            python_exe = os.path.join(venv_dir, "bin", "python")
            pyright_exe = os.path.join(venv_dir, "bin", "pyright")

        # 2. Install dependencies and Pyright
        # Pyright CLI is available via pip as 'pyright'
        packages_to_install = dependencies + ["pyright"]
        if not packages_to_install:  # Ensure there's at least 'pyright'
            packages_to_install = ["pyright"]
        elif "pyright" not in packages_to_install:
            packages_to_install.append("pyright")

        try:
            install_command = [pip_exe, "install"] + packages_to_install
            results["log"].append(f"Installing packages: {' '.join(install_command)}")
            install_proc = subprocess.run(
                install_command,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            results["dependencies_installed"] = True
            results["log"].append(
                f"Packages installed successfully:\n{install_proc.stdout}"
            )
        except subprocess.CalledProcessError as e:
            results["log"].append(
                f"Package installation failed for {pip_exe} install {' '.join(packages_to_install)}:\n{e.stderr}\nStdout was:\n{e.stdout}"
            )
            return results  # Critical failure

        # 3. Write AI code to a temporary file within the venv directory for Pyright check
        # Using NamedTemporaryFile within the venv_dir ensures it's cleaned up if the dir is.
        # However, we need to pass its name to subprocess, so delete=False and manual removal is safer.
        ai_code_file_for_check = tempfile.NamedTemporaryFile(
            mode="w+t", suffix=".py", delete=False, encoding="utf-8", dir=venv_dir
        )
        try:
            ai_code_file_for_check.write(ai_code_string)
            ai_code_file_for_check.close()  # Close it so Pyright can access it properly
            results["log"].append(f"AI code written to: {ai_code_file_for_check.name}")

            # 4. Perform Pyright static check
            pyright_result = _run_pyright_on_file(
                ai_code_file_for_check.name, pyright_exe
            )
            results["pyright_check_result"] = pyright_result
            results["log"].append(
                f"Pyright check completed. Success: {pyright_result['success']}"
            )
            if not pyright_result["success"]:
                results["log"].append(
                    f"Pyright found errors:\n{pyright_result['output']}"
                )
                # Optionally, you might not want to proceed if Pyright fails.
                # For now, we'll record it and proceed based on execute_code_after_check.

            # 5. Optionally execute the code if Pyright check was successful (or if forced)
            if execute_code_after_check:
                if not pyright_result["success"]:
                    results["log"].append(
                        "Skipping code execution due to Pyright errors."
                    )
                    results["code_execution_result"][
                        "executed"
                    ] = True  # Attempted, but skipped
                    results["code_execution_result"]["success"] = False
                    results["code_execution_result"][
                        "stderr"
                    ] = "Skipped due to Pyright errors."
                else:
                    results["log"].append(
                        f"Executing AI code with: {python_exe} {ai_code_file_for_check.name}"
                    )
                    results["code_execution_result"]["executed"] = True
                    try:
                        exec_proc = subprocess.run(
                            [python_exe, ai_code_file_for_check.name],
                            capture_output=True,
                            text=True,
                            encoding="utf-8",
                            timeout=30,  # Added timeout
                        )
                        results["code_execution_result"]["success"] = (
                            exec_proc.returncode == 0
                        )
                        results["code_execution_result"]["stdout"] = exec_proc.stdout
                        results["code_execution_result"]["stderr"] = exec_proc.stderr
                        results["code_execution_result"][
                            "return_code"
                        ] = exec_proc.returncode
                        results["log"].append(
                            f"Code execution finished. Return code: {exec_proc.returncode}"
                        )
                    except subprocess.TimeoutExpired:
                        results["log"].append("Code execution timed out.")
                        results["code_execution_result"]["success"] = False
                        results["code_execution_result"][
                            "stderr"
                        ] = "Execution timed out after 30 seconds."
                    except Exception as e:
                        results["log"].append(
                            f"Code execution threw an exception: {str(e)}"
                        )
                        results["code_execution_result"]["success"] = False
                        results["code_execution_result"]["stderr"] = str(e)
        finally:
            # Clean up the temporary AI code file
            if os.path.exists(ai_code_file_for_check.name):
                os.remove(ai_code_file_for_check.name)
                results["log"].append(
                    f"Cleaned up AI code file: {ai_code_file_for_check.name}"
                )

    # The venv_dir (and its contents if created within it) is automatically removed here
    # when the 'with tempfile.TemporaryDirectory() as venv_dir:' block exits.
    results["log"].append(
        "Temporary venv directory and its contents (should be) removed."
    )
    return results
