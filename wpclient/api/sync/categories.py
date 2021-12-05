from typing import Literal, Optional

from wpclient.models.category import Category, CategoryFilter
from .crud import CRUD


class Categories(CRUD):
    endpoint = "/wp/v2/categories"

    def filter(self, filter: CategoryFilter) -> list[Category]:
        """
        Retrieve all categories matching the filter
        """

        filters: dict = filter.dict(exclude_none=True)
        objects: list[dict] = self._filter(endpoint=self.endpoint, filters=filters)

        return [Category.parse_obj(obj) for obj in objects]

    def create(self, category: Category) -> Category:
        """
        Create a new category
        """
        data: dict = category.dict(exclude_none=True)
        wp_obj: dict = self._create(self.endpoint, data)

        return category.parse_obj(wp_obj)

    def get(
        self, id: int, context: Optional[Literal["view", "embed", "edit"]] = None
    ) -> Category:
        """
        Retrieve a especific category by ID
        """

        filters = {}

        if context:
            filters["context"] = context

        wp_obj: dict = self._get(endpoint=self.endpoint, id=id, filters=filters)

        return Category.parse_obj(wp_obj)

    def update(self, id: int, data: dict) -> Category:
        """
        Update a category
        """

        wp_obj: dict = self._update(endpoint=self.endpoint, id=id, data=data)

        return Category.parse_obj(wp_obj)

    def delete(self, id: int) -> bool:
        """
        Delete a category
        """

        wp_obj: dict = self._delete(endpoint=self.endpoint, id=id, force=True)

        return wp_obj["deleted"]
