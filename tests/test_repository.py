import pytest

from vector_editor.domain.shapes import Point


def test_next_id_starts_from_one(repo):
    assert repo.next_id() == 1
    assert repo.next_id() == 2


def test_add_shape(repo):
    point = Point(id=repo.next_id(), x=1, y=2)

    saved = repo.add(point)

    assert saved is point
    assert saved.id == 1
    assert repo.exists(1) is True


def test_list_shapes(repo):
    first = repo.add(Point(id=repo.next_id(), x=1, y=2))
    second = repo.add(Point(id=repo.next_id(), x=3, y=4))

    shapes = list(repo.list_all())

    assert shapes == [first, second]
    assert [shape.id for shape in shapes] == [1, 2]


def test_remove_shape(repo):
    point = repo.add(Point(id=repo.next_id(), x=1, y=2))

    removed = repo.remove(point.id)

    assert removed is point
    assert repo.exists(point.id) is False


def test_remove_missing_shape_raises_key_error(repo):
    with pytest.raises(KeyError):
        repo.remove(999)