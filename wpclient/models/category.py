from typing import Literal, Optional, Union
from pydantic import BaseModel


class CategoryFilter(BaseModel):
    context: Optional[Literal["view", "embed", "edit"]]
    page: Optional[int]
    per_page: Optional[int]
    search: Optional[str]
    exclude: Optional[Union[int, list[int]]]
    include: Optional[Union[int, list[int]]]
    order: Optional[Literal["asc", "desc"]]
    orderby: Optional[
        Literal[
            "id",
            "include",
            "name",
            "slug",
            "include_slugs",
            "term_group",
            "description",
            "count",
        ]
    ]
    hide_empty: Optional[bool]
    parent: Optional[int]
    post: Optional[int]
    slug: Optional[Union[str, list[str]]]


class Category(BaseModel):
    """
    Define a WordPress Category Model

    ...

    Attributes
    ----------

    id : int, optional
        Unique identifier for the term

    count : int, optional
        Number of published posts for the term

    description : str, optional
        HTML description of the term

    link : str, optional
        URL of the term

    name : str
        HTML title for the term

    slug : str, optional
        An alphanumeric identifier for the term unique to its type

    taxonomy : str, optional
        Type attribution for the term
        One of: *category*, *post_tag*, *nav_menu*, *link_category*, *post_format*

    parent : int, optional
        The parent term ID

    meta : dict, optional
        Meta fields
    """

    id: Optional[int]
    count: Optional[int]
    description: Optional[str]
    link: Optional[str]
    name: str
    slug: Optional[str]
    taxonomy: Optional[
        Literal["category", "post_tag", "nav_menu", "link_category", "post_format"]
    ]
    parent: Optional[int]
    meta: Optional[dict]
