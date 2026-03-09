from __future__ import annotations

from collections.abc import Iterable

from vector_editor.domain.base import Shape


class InMemoryShapeRepository:
    def __init__(self) -> None:
        self._items: dict[int, Shape] = {}
        self._next_id = 1

    def next_id(self) -> int:
        current = self._next_id
        self._next_id += 1
        return current

    def add(self, shape: Shape) -> Shape:
        self._items[shape.id] = shape
        return shape

    def list_all(self) -> Iterable[Shape]:
        return [self._items[key] for key in sorted(self._items)]

    def exists(self, shape_id: int) -> bool:
        return shape_id in self._items

    def remove(self, shape_id: int) -> Shape:
        return self._items.pop(shape_id)
