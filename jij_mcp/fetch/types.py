from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class FetchRequestArgs(BaseModel):
    """Input arguments schema for fetch tools."""

    url: HttpUrl = Field(..., description="URL of the content to fetch.")
    headers: Optional[dict[str, str]] = Field(
        default=None, description="Optional headers to include in the request."
    )


# エラーを含む可能性のあるレスポンス型
class FetchResponse(BaseModel):
    content: list[dict[str, str]]  # MCP標準のcontent形式に合わせる
    isError: bool = False
    errorMessage: Optional[str] = None
