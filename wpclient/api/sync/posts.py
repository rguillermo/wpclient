from typing import Literal, Optional
from .crud import CRUD
from wpclient.models.post import Post, PostFilter


class Posts(CRUD):
    endpoint = "/wp/v2/posts"

    def filter(self, filter: PostFilter) -> list[Post]:
        """
        Retrieve all posts matching the filter
        """
        filters: dict = filter.dict(exclude_none=True)
        objects: list[dict] = self._filter(endpoint=self.endpoint, filters=filters)

        return [Post.parse_obj(obj) for obj in objects]

    def create(self, post: Post) -> Post:
        """
        Create a post
        """
        data: dict = post.dict(exclude_none=True)

        wp_post: dict = self._create(endpoint=self.endpoint, data=data)
        return post.parse_obj(wp_post)

    def get(
        self,
        id: int,
        context: Optional[Literal["view", "embed", "edit"]] = None,
        password: Optional[str] = None,
    ) -> Post:
        """
        Retrieve a specific post
        """
        filters = {}

        if context:
            filters["context"] = context

        if password:
            filters["password"] = password

        post_data: dict = self._get(endpoint=self.endpoint, id=id, filters=filters)
        post = Post.parse_obj(post_data)

        return post

    def update(self, id: int, data: dict) -> Post:
        """
        Update a post with the given kwargs
        """
        wp_obj: dict = self._update(endpoint=self.endpoint, id=id, data=data)

        return Post.parse_obj(wp_obj)

    def delete(self, id: int, force: bool = True) -> bool:
        """
        Delete a post
        """
        wp_obj = self._delete(endpoint=self.endpoint, id=id, force=force)

        if force:
            return wp_obj["deleted"]

        if wp_obj["id"]:
            return True

        return False
