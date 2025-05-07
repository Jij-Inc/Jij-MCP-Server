FROM python:3.12-slim

ARG GIT_COMMIT

LABEL org.opencontainers.image.source="https://github.com/Jij-Inc/Jij-MCP-Server"
LABEL org.opencontainers.image.title="Jij MCP Server"
LABEL org.opencontainers.image.description="A MCP server for supporting the implementation of JijModeling."
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.revision=$GIT_COMMIT

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app
RUN uv sync --frozen

CMD ["uv", "run", "jij_mcp/server.py"]
