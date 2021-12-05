from datetime import date, datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, validator


class PostFilter(BaseModel):
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
    slug: Optional[Union[str, list[str]]]
    status: Optional[Literal["publish", "future", "draft", "pending", "private"]]
    tax_relation: Optional[Literal["AND", "OR"]]
    categories: Optional[Union[str, list[str]]]
    categories_exclude: Optional[Union[str, list[str]]]
    tags: Optional[Union[str, list[str]]]
    tags_exclude: Optional[Union[str, list[str]]]
    sticky: Optional[bool]


class Post(BaseModel):
    """
    Define a WordPress Post model

    Attributes
    ----------

    date : datetime, optional
        The date the object was published, in the site's timezone

    date_gmt : datetime, optional
        The date the object was published, as GMT

    guid : dict, optional
        The globally unique identifier for the object

    id : int, optional
        Unique identifier for the object

    link : str, optional
        URL to the object

    modified : datetime, optional
        The date the object was last modified, in the site's timezone

    modified_gmt : datetime, optional
        The date the object was last modified, as GMT

    slug : str, optional
        An alphanumeric identifier for the object unique to its type

    status : str, optional
        A named status for the object. One of: publish, future, draft, pending, private

    type : str, optional
        Type of Post for the object

    password : str, optional
        A password to protect access to the content and excerpt

    permalink_template : str, optional
        Permalink template for the object

    generated_slug : str, optional
        Slug automatically generated from the object title

    title : str
        The title for the object

    content : str, optional
        The content for the object

    author : int, optional
        The ID for the author of the object

    excerpt : dict, optional
        The excerpt for the object

    featured_media : int, optional
        The ID of the featured media for the object.

    comment_status : str, optional
        Whether or not comments are open on the object.
        One of: open, closed

    ping_status : str, optional
        Whether or not the object can be pinged.
        One of: open, closed

    format : str, optional
        The format for the object.
        One of: standard, aside, chat, gallery, link, image, quote, status, video, audio

    meta : dict, optional
        Meta fields

    sticky : bool, optional
        Whether or not the object should be treated as sticky

    template : str, optional
        The theme file to use to display the object

    categories : list, optional
        The terms assigned to the object in the category taxonomy

    tags : list, optional
        The terms assigned to the object in the post_tag taxonomy.

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
    format: Optional[
        Literal[
            "standard",
            "aside",
            "chat",
            "gallery",
            "link",
            "image",
            "quote",
            "status",
            "video",
            "audio",
        ]
    ]
    meta: Optional[dict]
    sticky: Optional[bool]
    template: Optional[str]
    categories: Optional[list]
    tags: Optional[list]

    @validator("title", "content", "excerpt", pre=True)
    def check_if_dict(cls, value):
        if isinstance(value, dict):

            return value["rendered"]

        return value
