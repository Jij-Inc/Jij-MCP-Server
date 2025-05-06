from mcp_setting import mcp


if __name__ == "__main__":
    print("Starting MCP server in stdio mode")
    mcp.run(transport="stdio")
