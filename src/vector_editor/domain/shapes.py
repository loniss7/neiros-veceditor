from __future__ import annotations

from dataclasses import dataclass

from vector_editor.domain.base import Shape


@dataclass(slots=True)
class Point(Shape):
    x: float
    y: float

    @property
    def shape_type(self) -> str:
        return "Point"

    def summary(self) -> str:
        return f"x={self.x:g}, y={self.y:g}"


@dataclass(slots=True)
class Segment(Shape):
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def shape_type(self) -> str:
        return "Segment"

    def summary(self) -> str:
        return f"start=({self.x1:g}, {self.y1:g}), end=({self.x2:g}, {self.y2:g})"


@dataclass(slots=True)
class Circle(Shape):
    center_x: float
    center_y: float
    radius: float

    @property
    def shape_type(self) -> str:
        return "Circle"

    def summary(self) -> str:
        return f"center=({self.center_x:g}, {self.center_y:g}), radius={self.radius:g}"


@dataclass(slots=True)
class Square(Shape):
    x: float
    y: float
    side: float

    @property
    def shape_type(self) -> str:
        return "Square"

    def summary(self) -> str:
        return f"origin=({self.x:g}, {self.y:g}), side={self.side:g}"

@dataclass(slots=True)
class Oval(Shape):
    center_x: float
    center_y: float
    radius_x: float
    radius_y: float

    @property
    def shape_type(self) -> str:
        return "Oval"

    def summary(self) -> str:
        return (
            f"center=({self.center_x:g}, {self.center_y:g}), "
            f"rx={self.radius_x:g}, ry={self.radius_y:g}"
        )


@dataclass(slots=True)
class Rectangle(Shape):
    x: float
    y: float
    width: float
    height: float

    @property
    def shape_type(self) -> str:
        return "Rectangle"

    def summary(self) -> str:
        return f"origin=({self.x:g}, {self.y:g}), width={self.width:g}, height={self.height:g}"
