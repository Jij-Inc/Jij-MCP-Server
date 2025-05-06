# Jij MCP Server

A server that provides tools to support mathematical optimization with JijModeling and quantum computing.

## Overview

The Jij MCP Server contains various tools and utilities designed to assist with the implementation of mathematical optimization models using JijModeling and quantum computing tasks using Qiskit. This platform integrates both domains to provide comprehensive support for computational optimization and quantum programming.

## Features

### JijModeling Support
- Reference information about JijModeling syntax and usage
- Code checking for detection of common issues in JijModeling code
- Model creation assistance with best practices guidance
- Step-by-step workflow for implementing optimization models

### Quantum Computing Support
- Qiskit migration guides from v0.x to v1/v2
- API reference documentation access
- Integration with IBM Quantum Learning Hub tutorials
- Structured workflow for quantum circuit design and execution

## Configuration

The MCP server can be configured in your settings file as follows:

```json
{
    "mcpServers": {
        "jij": {
            "command": "uv",
            "args": [
                "--directory",
                "<YOUR PATH>/jij-mcp-server",
                "run",
                "jij_mcp/server.py"
            ]
        }
    }
}
```

This configuration specifies:
- Server name: `jij`
- Command to run: `uv`
- Arguments:
    - `--directory`: Specifies the server location
    - Path to your server directory
    - `run`: Command to execute the server
    - `jij_mcp/server.py`: Server script to run

## Available Tools

### JijModeling Tools
- `learn_jijmodeling`: Guide to JijModeling syntax and usage
- `jm_check`: Validation tool for JijModeling code

### Qiskit Tools
- `qiskit_v0tov1v2_migration_guide`: Guide for transitioning between Qiskit versions
- `qiskit_v1_api_reference_toc` and `qiskit_v2_api_reference_toc`: API documentation access
- `qiskit_tutorial`: Access to IBM Quantum Learning Hub tutorials

## License

Apache License 2.0