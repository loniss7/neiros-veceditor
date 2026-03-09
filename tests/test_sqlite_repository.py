import pytest

from vector_editor.domain.shapes import Circle, Point
from vector_editor.repositories.sqlite import SQLiteShapeRepository


def test_add_shape(tmp_path):
    db_path = tmp_path / "shapes.db"
    repo = SQLiteShapeRepository(db_path)

    point = Point(id=repo.next_id(), x=1, y=2)
    saved = repo.add(point)

    assert saved == point
    assert repo.exists(point.id) is True

    repo.close()


def test_list_shapes(tmp_path):
    db_path = tmp_path / "shapes.db"
    repo = SQLiteShapeRepository(db_path)

    first = repo.add(Point(id=repo.next_id(), x=1, y=2))
    second = repo.add(Circle(id=repo.next_id(), center_x=0, center_y=0, radius=5))

    shapes = repo.list_all()

    assert shapes == [first, second]

    repo.close()


def test_remove_shape(tmp_path):
    db_path = tmp_path / "shapes.db"
    repo = SQLiteShapeRepository(db_path)

    point = repo.add(Point(id=repo.next_id(), x=1, y=2))
    removed = repo.remove(point.id)

    assert removed == point
    assert repo.exists(point.id) is False

    repo.close()


def test_remove_missing_shape_raises_key_error(tmp_path):
    db_path = tmp_path / "shapes.db"
    repo = SQLiteShapeRepository(db_path)

    with pytest.raises(KeyError):
        repo.remove(999)

    repo.close()


def test_persistence_between_instances(tmp_path):
    db_path = tmp_path / "shapes.db"

    repo1 = SQLiteShapeRepository(db_path)
    created = repo1.add(Point(id=repo1.next_id(), x=10, y=20))
    repo1.close()

    repo2 = SQLiteShapeRepository(db_path)
    shapes = repo2.list_all()

    assert shapes == [created]
    assert repo2.next_id() == 2

    repo2.close()