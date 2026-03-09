import pytest

from vector_editor.repositories.memory import InMemoryShapeRepository
from vector_editor.services.shape_service import ShapeService


@pytest.fixture
def repo():
    return InMemoryShapeRepository()


@pytest.fixture
def service(repo):
    return ShapeService(repo)