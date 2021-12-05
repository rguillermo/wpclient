from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, validator


class MediaFilter(BaseModel):
    context: Optional[str]
    page: int = 1
    per_page: Optional[int]
    search: Optional[str]
    after: Optional[date]
    author: Optional[list[int]]
    author_exclude: Optional[list[int]]
    before: Optional[date]
    exclude: Optional[list[int]]
    include: Optional[list[int]]
    offset: Optional[int]
    order: Literal["asc", "desc"] = "desc"
    orderby: Literal[
        "author",
        "date",
        "id",
        "include",
        "modified",
        "parent",
        "relevance",
        "slug",
        "include_slugs",
        "title",
    ] = "date"
    parent: Optional[list[int]]
    parent_exclude: Optional[int]
    slug: Optional[str]
    status: Optional[str]
    media_type: Optional[Literal["image", "video", "text", "application", "audio"]]
    mime_type: Optional[str]


class MediaModel(BaseModel):
    date: Optional[datetime]
    date_gmt: Optional[datetime]
    guid: Optional[dict]
    id: Optional[int]
    link: Optional[str]
    modified: Optional[datetime]
    modified_gmt: Optional[datetime]
    slug: Optional[str]
    status: Literal[
        "publish", "future", "draft", "pending", "private", "inherit"
    ] = "publish"
    type: Optional[str]
    permalink_template: Optional[str]
    generated_slug: Optional[str]
    title: Optional[str]
    author: Optional[int]
    comment_status: Optional[Literal["open", "closed"]]
    ping_status: Optional[Literal["open", "closed"]]
    meta: Optional[dict]
    template: Optional[str]
    alt_text: Optional[str]
    caption: Optional[dict]
    description: Optional[dict]
    media_type: Literal["image", "file"] = "image"
    mime_type: Optional[str]
    media_details: Optional[dict]
    post: Optional[int]
    source_url: Optional[str]
    missing_image_sizes: Optional[list]
    source: Optional[str]

    @validator("title", pre=True)
    def check_if_dict(cls, value):
        if isinstance(value, dict):

            return value["rendered"]

        return value
