from mcp.server.fastmcp import FastMCP
from jm_prompts import jijmodeling_guide_prompt
from jm_checker import jijmodeling_check


mcp = FastMCP(
    "JijModeling-Assistant",
    instructions=(
        "# JijModeling Assistant"
        + "This server provides tools to assist with mathematical modeling using JijModeling."
        + """
## Core Features
- Reference information about JijModeling syntax and usage
- Code checking: Detection of common issues in JijModeling code
- Model creation assistance: Generation of JijModeling code from problem descriptions

## Best Practices
- **When Creating Code**: Avoid direct Python loops (for statements); instead use Element objects and jm.sum()
- **Variable Definition**: Clearly define the type (BinaryVar, IntegerVar, ContinuousVar), shape and (lower_bound, upper_bound) for each variable
- **Problem Construction**: Set a clear objective (maximize/minimize) through jm.ProblemSense.MAXIMIZE or .MINIMIZE and provide meaningful names for constraints
- **Code Validation**: After implementation, use the `jm_check` tool to verify your code

## When To Use Each Tool
- **jijmodeling_guide**: Use when learning about JijModeling syntax and practical usage
- **learn_jijmodeling**: Use when you need a quick reference or overview of JijModeling
- **jm_check**: Use when validating your JijModeling code for potential issues. this tool accepts only runnable jijmodeling code which is not included any another converting and executing solver code.

## Workflow
You will guide users through implementing optimization models in JijModeling following these steps:
1. Problem formulation and implementation strategy
2. Learning about JijModeling syntax and usage with `learn_jijmodeling`
3. Code generation:
    3-1. Define the data variables using `Placeholder` objects
    3-2. Define the decision variables using `BinaryVar`, `IntegerVar`, or `ContinuousVar`
    3-3. Define the element objects using `jm.Element`
    3-4. Define problem object using `jm.Problem`
    3-5. Define the objective function using `jm.sum()`
    3-6. Define the constraints using `jm.Constraint`
4. Code validation using `jm_check`
5. refinement and debugging of the code
"""
    ),
    debug=True,
)

@mcp.resource("jijmodeling://docs/guide")
def jijmodeling_guide() -> str:
    """JijModeling guide."""
    return jijmodeling_guide_prompt


@mcp.tool()
def learn_jijmodeling() -> str:
    """
    Provide a guide to JijModeling.

    Returns:
        str: The guide to JijModeling.
    """
    return jijmodeling_guide_prompt


@mcp.tool()
def jm_check(code: str) -> dict:
    """
    Check the code for JijModeling rules.

    Args:
        code (str): The code to check.

    Returns:
        dict: The result of the check.
    """
    return jijmodeling_check(code)


if __name__ == "__main__":
    print("Starting MCP server in stdio mode")
    mcp.run(transport="stdio")
