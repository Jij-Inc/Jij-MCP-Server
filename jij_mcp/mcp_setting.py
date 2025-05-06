from mcp.server.fastmcp import FastMCP
from jm_prompts import jijmodeling_guide_prompt
from jm_checker import jijmodeling_check
from fetch import Fetcher, FetchRequestArgs, FetchResponse
from quantum.qiskit_prompt import qiskit_v1_v2_migration_prompt

import typing as typ


mcp = FastMCP(
    "Jij Mathematical and Quantum Computing Platform",
    instructions=(
        """This server provides tools to assist with both mathematical optimization using JijModeling and quantum computing using Qiskit.

## Core Features
- Mathematical optimization with JijModeling
- Quantum computing with Qiskit
- Code checking and validation
- Reference documentation and tutorials

## JijModeling Features
- Reference information about JijModeling syntax and usage
- Code checking: Detection of common issues in JijModeling code
- Model creation assistance: Generation of JijModeling code from problem descriptions

## Qiskit Features
- Migration guides from Qiskit v0.x to v1/v2
- API reference documentation
- Access to Qiskit tutorials from IBM Quantum Learning Hub

## Best Practices for JijModeling
- **When Creating Code**: Avoid direct Python loops (for statements); instead use Element objects and jm.sum()
- **Variable Definition**: Clearly define the type (BinaryVar, IntegerVar, ContinuousVar), shape and (lower_bound, upper_bound) for each variable
- **Problem Construction**: Set a clear objective (maximize/minimize) through jm.ProblemSense.MAXIMIZE or .MINIMIZE and provide meaningful names for constraints
- **Code Validation**: After implementation, use the `jm_check` tool to verify your code

## Best Practices for Qiskit
- Always refer to the migration guide when working with Qiskit v1/v2
- Follow IBM Quantum's best practices for circuit design and execution
- Use appropriate error mitigation techniques for your specific quantum problem

## When To Use Each Tool
### JijModeling Tools
- **jijmodeling_guide**: Use when learning about JijModeling syntax and practical usage
- **learn_jijmodeling**: Use when you need a quick reference or overview of JijModeling
- **jm_check**: Use when validating your JijModeling code for potential issues

### Qiskit Tools
- **qiskit_v0tov1v2_migration_guide**: Use when transitioning from older Qiskit versions
- **qiskit_v1_api_reference_toc**: Use to explore Qiskit v1 API documentation
- **qiskit_v2_api_reference_toc**: Use to explore the latest Qiskit v2 API documentation
- **qiskit_tutorial**: Use to access IBM Quantum Learning Hub tutorials

## JijModeling Workflow
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
5. Refinement and debugging of the code

## Qiskit Workflow
Guide users through quantum computing tasks with these steps:
1. Problem analysis and quantum algorithm selection
2. Review Qiskit version compatibility using migration guides
3. Circuit design and implementation
4. Execution strategy (simulator or real hardware)
5. Result interpretation and visualization
"""
    ),
    debug=True,
)

# Mathematical Optimization ----------
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


# Quantum Computing ----------
@mcp.resource("jij://quantum/qiskit/v1v2migration-guide")
def qiskit_v0tov1v2_migration_guide_prompt() -> str:
    """Qiskit v1 to v2 migration guide.
    AI models are likely trained on Qiskit v0.x and may not be familiar with v1 and v2.
    Therefore, it is necessary to provide a migration guide from v1 to v2.
    Please refer to this guide first when writing Qiskit code.
    
    """
    return qiskit_v1_v2_migration_prompt

@mcp.tool()
async def qiskit_v0tov1v2_migration_guide() -> str:
    """
    AI models are likely trained on Qiskit v0.x and may not be familiar with v1 and v2.
    Therefore, it is necessary to provide a migration guide from v1 to v2.
    Please refer to this guide first when writing Qiskit code.
    
    Returns:
        str: The migration guide content.
    """
    return qiskit_v1_v2_migration_prompt

@mcp.tool()
async def qiskit_v1_api_reference_toc() -> str:
    """
    Fetch the Qiskit v1 API reference table of contents (https://docs.quantum.ibm.com/api/qiskit/1.4).
    Returns:
        str: The table of contents in Markdown format.
    """
    url = "https://docs.quantum.ibm.com/api/qiskit/1.4"
    response: FetchResponse = await fetch_as_markdown(url)
    if response.isError:
        return response.errorMessage if response.errorMessage else "Error fetching the content"
    return url + "\n" + response.content[0]["text"]

@mcp.tool()
async def qiskit_v2_api_reference_toc() -> str:
    """
    Fetch the Qiskit v2 (latest) API reference table of contents (https://docs.quantum.ibm.com/api/qiskit).
    Returns:
        str: The table of contents in Markdown format.
    """
    url = "https://docs.quantum.ibm.com/api/qiskit"
    response: FetchResponse = await fetch_as_markdown(url)
    if response.isError:
        return response.errorMessage if response.errorMessage else "Error fetching the content"
    return url + "\n" + response.content[0]["text"]

@mcp.tool()
async def qiskit_tutorial(tutorial_name: str) -> str:
    """
    Fetch a Qiskit tutorial from the IBM Quantum Learning Hub.
    First, get the table of contents (toc) and check the tutorial names.
    Tutorial names should be specified in lowercase with hyphens (e.g., "variational-quantum-eigensolver").
    If the tutorial name is not found, it will return an error message.

    Args:
        tutorial_name (str): The name of the tutorial to fetch. Use "toc" for the table of contents.
        If the tutorial name is not found, it will return an error message.
        tutorial_name should be in lowercase and hyphenated (e.g., "variational-quantum-eigensolver").
    Returns:
        str: The tutorial content in Markdown format.
    """
    if tutorial_name == "toc":
        url = "https://learning.quantum.ibm.com/catalog/tutorials"
    else:
        url = f"https://learning.quantum.ibm.com/tutorial/{tutorial_name}"

    response: FetchResponse = await fetch_as_markdown(url)
    if response.isError:
        return response.errorMessage if response.errorMessage else "Error fetching the content"
    
    if tutorial_name == "toc":
        # If the tutorial name is "toc", return the table of contents
        return url + "\n" + response.content[0]["text"] + "\n\n" + "Please specify the tutorial name in lowercase and hyphenated (e.g., 'variational-quantum-eigensolver')."
    else:
        return url + "\n" + response.content[0]["text"] 


# Utils ----------------------
@mcp.tool()
async def fetch_as_markdown(
    url: str, headers: typ.Optional[dict[str, str]] = None
) -> FetchResponse:
    """
    Fetch a website, convert its HTML content to Markdown, and return it.

    Args:
        url (str): URL of the website to fetch.
        headers (Optional[dict[str, str]]): Custom headers for the request.

    Returns:
        FetchResponse: An object containing the Markdown content or an error message.
                       On success, isError is false and content contains the Markdown text.
                       On failure, isError is true and errorMessage contains the error details.
    """
    args = FetchRequestArgs(url=url, headers=headers)
    return await Fetcher.markdown(args)
