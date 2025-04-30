import re
import typing


class PythonREPL:

    @classmethod
    def run(cls, code: str) -> dict[str, typing.Any]:
        try:
            exec(code)
            return {"status": "success"}
        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            error_position = extract_error_position_codes(code, error_details)

            return {"status": "error", "error": error_position}


def extract_error_position_codes(code: str, error_details: str):
    lines = code.split("\n")

    # Find the line that references "<string>" which indicates the error in the executed code
    # Pattern matches: 'File "<string>", line X, in <module>'
    string_error_match = re.search(
        r'File "(?:<string>|<module>|__string__)", line (\d+)', error_details
    )

    if not string_error_match:
        # If no match with <string>, try to find any line reference
        line_match = re.search(r"line (\d+)", error_details)
        if not line_match:
            return None
        line_number = int(line_match.group(1))
    else:
        line_number = int(string_error_match.group(1))

    # Adjust for 0-based indexing
    if line_number > 0 and line_number <= len(lines):
        # Get the problematic line and adjacent lines for context
        start_line = max(0, line_number - 2)
        end_line = min(len(lines), line_number + 2)

        error_context = []
        for i in range(start_line, end_line):
            prefix = ">>> " if i == line_number - 1 else "    "
            error_context.append(f"{i+1}: {prefix}{lines[i]}")

        return {
            "line_number": line_number,
            "error_line": lines[line_number - 1],
            "context": "\n".join(error_context),
            "error_type": (
                re.search(r"(\w+Error:.*?)$", error_details, re.MULTILINE).group(1)
                if re.search(r"(\w+Error:.*?)$", error_details, re.MULTILINE)
                else "Unknown error"
            ),
        }

    return {
        "line_number": line_number,
        "error_line": "No line found",
        "context": "No context found",
        "error_type": "Unknown error",
    }


def extract_python_code(conetnt: str) -> str:
    code_blocks = conetnt.split("```python")
    # Remove the first split as it's before the first ```python
    code_blocks = code_blocks[1:]
    # For each block, get the content before the closing ```
    code_parts = [block.split("```")[0] for block in code_blocks]
    # Join all code parts
    return "\n".join(code_parts)
