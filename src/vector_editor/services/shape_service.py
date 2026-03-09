from __future__ import annotations

from vector_editor.domain.base import Shape
from vector_editor.domain.errors import ShapeNotFoundError, ValidationError
from vector_editor.domain.shapes import Circle, Point, Segment, Square
from vector_editor.repositories.memory import InMemoryShapeRepository


class ShapeService:
    def __init__(self, repository: InMemoryShapeRepository) -> None:
        self._repository = repository

    def create_point(self, x: float, y: float) -> Shape:
        return self._repository.add(Point(id=self._repository.next_id(), x=x, y=y))

    def create_segment(self, x1: float, y1: float, x2: float, y2: float) -> Shape:
        return self._repository.add(
            Segment(id=self._repository.next_id(), x1=x1, y1=y1, x2=x2, y2=y2)
        )

    def create_circle(self, center_x: float, center_y: float, radius: float) -> Shape:
        self._ensure_positive(value=radius, field_name="radius")
        return self._repository.add(
            Circle(
                id=self._repository.next_id(),
                center_x=center_x,
                center_y=center_y,
                radius=radius,
            )
        )

    def create_square(self, x: float, y: float, side: float) -> Shape:
        self._ensure_positive(value=side, field_name="side")
        return self._repository.add(Square(id=self._repository.next_id(), x=x, y=y, side=side))

    def list_shapes(self) -> list[Shape]:
        return list(self._repository.list_all())

    def delete_shape(self, shape_id: int) -> Shape:
        if not self._repository.exists(shape_id):
            raise ShapeNotFoundError(f"Shape with id={shape_id} was not found.")
        return self._repository.remove(shape_id)

    @staticmethod
    def _ensure_positive(*, value: float, field_name: str) -> None:
        if value <= 0:
            raise ValidationError(f"{field_name.capitalize()} must be greater than zero.")
