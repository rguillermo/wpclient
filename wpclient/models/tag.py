from typing import Any, Optional

from pydantic import BaseModel


class TagFilter(BaseModel):
    context: Optional[str]
    page: int = 1
    per_page: Optional[int]
    search: Optional[str]
    exclude: Optional[list[int]]
    include: Optional[list[int]]
    offset: Optional[int]
    order: Optional[str]
    orderby: Optional[str]
    hide_empty: Optional[bool]
    post: Optional[int]
    slug: Optional[str]


class Tag(BaseModel):
    id: Optional[int]
    count: Optional[int]
    description: Optional[str]
    link: Optional[str]
    name: Optional[str]
    slug: Optional[str]
    taxonomy: Optional[str]
    meta: Optional[dict[str, Any]]
