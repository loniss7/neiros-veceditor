from __future__ import annotations

from vector_editor.cli.controller import CLIController
from vector_editor.cli.menu import QuestionaryMenu
from vector_editor.cli.views import RichCLIView
from vector_editor.repositories.sqlite import SQLiteShapeRepository
from vector_editor.services.shape_service import ShapeService


def build_application() -> CLIController:
    repository = SQLiteShapeRepository()  # persistent storage in SQLite
    service = ShapeService(repository=repository)
    view = RichCLIView()
    menu = QuestionaryMenu()
    return CLIController(service=service, view=view, menu=menu)


def main() -> None:
    controller = build_application()
    controller.run()