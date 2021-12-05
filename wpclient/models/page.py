from datetime import date, datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, validator


class PageFilter(BaseModel):
    context: Optional[Literal["view", "embed", "edit"]]
    page: Optional[int]
    per_page: Optional[int]
    search: Optional[str]
    after: Optional[date]
    author: Optional[Union[int, list[int]]]
    author_exclude: Optional[Union[int, list[int]]]
    before: Optional[date]
    exclude: Optional[Union[int, list[int]]]
    include: Optional[Union[int, list[int]]]
    menu_order: Optional[int]
    offset: Optional[int]
    order: Optional[Literal["asc", "desc"]]
    orderby: Optional[
        Literal[
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
        ]
    ]
    parent: Optional[list[int]]
    parent_exclude: Optional[list[int]]
    slug: Optional[Union[str, list[str]]]
    status: Optional[Literal["publish", "future", "draft", "pending", "private"]]


class Page(BaseModel):
    """
    Define a WordPress Page model

    """

    date: Optional[datetime]
    date_gmt: Optional[datetime]
    id: Optional[int]
    link: Optional[str]
    modified: Optional[datetime]
    modified_gmt: Optional[datetime]
    slug: Optional[str]
    status: Literal["publish", "future", "draft", "pending", "private"] = "publish"
    type: Optional[str]
    password: Optional[str]
    permalink_template: Optional[str]
    generated_slug: Optional[str]
    title: str
    content: Optional[str]
    author: Optional[int]
    excerpt: Optional[str]
    featured_media: Optional[int]
    comment_status: Optional[Literal["open", "closed"]]
    ping_status: Optional[Literal["open", "closed"]]
    menu_order: Optional[int]
    meta: Optional[dict]
    template: Optional[str]

    @validator("title", "content", "excerpt", pre=True)
    def check_if_dict(cls, value):
        if isinstance(value, dict):

            return value["rendered"]

        return value
