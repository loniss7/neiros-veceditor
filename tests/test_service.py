import pytest

from vector_editor.domain.errors import ShapeNotFoundError, ValidationError
from vector_editor.domain.shapes import Circle, Point, Square


def test_create_point(service):
    shape = service.create_point(1, 2)

    shapes = service.list_shapes()

    assert isinstance(shape, Point)
    assert shape.id == 1
    assert shape.summary() == "x=1, y=2"
    assert shapes == [shape]


def test_create_circle(service):
    shape = service.create_circle(0, 0, 5)

    shapes = service.list_shapes()

    assert isinstance(shape, Circle)
    assert shape.id == 1
    assert shape.summary() == "center=(0, 0), radius=5"
    assert shapes == [shape]


def test_create_circle_invalid_radius(service):
    with pytest.raises(ValidationError, match="Radius must be greater than zero."):
        service.create_circle(0, 0, 0)


def test_create_square_invalid_side(service):
    with pytest.raises(ValidationError, match="Side must be greater than zero."):
        service.create_square(0, 0, -1)


def test_delete_shape(service):
    shape = service.create_point(1, 2)

    removed = service.delete_shape(shape.id)

    assert removed == shape
    assert service.list_shapes() == []


def test_delete_missing_shape(service):
    with pytest.raises(ShapeNotFoundError, match="Shape with id=999 was not found."):
        service.delete_shape(999)


def test_create_square(service):
    shape = service.create_square(0, 0, 3)

    assert isinstance(shape, Square)
    assert shape.id == 1
    assert shape.summary() == "origin=(0, 0), side=3"