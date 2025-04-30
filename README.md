# Jij MCP Server

A server that provides tools to support the implementation of Jij Modeling.

<a href="https://glama.ai/mcp/servers/@Jij-Inc/Jij-MCP-Server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@Jij-Inc/Jij-MCP-Server/badge" alt="Jij Server MCP server" />
</a>

## Overview

The Jij MCP Server contains various tools and utilities designed to assist with the implementation of JijModeling. 

## Installation

1. Clone this repository
2. Install the required dependencies
3. Configure the server as described below

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

## Usage

Once configured, the MCP server will provide various tools to help with JijModeling implementation.

## Features

- Support tools for JijModeling implementation
- Easy configuration and setup
- Extensible architecture for custom modeling workflows

## License

Apache License 2.0