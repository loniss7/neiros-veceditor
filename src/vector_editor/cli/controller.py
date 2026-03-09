from __future__ import annotations

from vector_editor.cli.menu import MenuAction, QuestionaryMenu
from vector_editor.cli.views import RichCLIView
from vector_editor.domain.errors import ShapeNotFoundError, ValidationError, VectorEditorError
from vector_editor.services.shape_service import ShapeService


class CLIController:
    def __init__(self, service: ShapeService, view: RichCLIView, menu: QuestionaryMenu) -> None:
        self._service = service
        self._view = view
        self._menu = menu

    def run(self) -> None:
        self._view.clear()
        self._view.render_header()
        self._view.render_help()

        while True:
            try:
                action = self._menu.choose_action()
                if action is MenuAction.EXIT:
                    self._view.info("Goodbye.")
                    return

                self._dispatch(action)

            except KeyboardInterrupt:
                self._view.info("Operation cancelled by user.")
            except (ValidationError, ShapeNotFoundError) as exc:
                self._view.error(str(exc))
            except VectorEditorError as exc:
                self._view.error(str(exc))

            input("\nPress Enter to continue...")
            self._view.clear()
            self._view.render_header()

    def _dispatch(self, action: MenuAction) -> None:
        if action is MenuAction.CREATE_POINT:
            self._create_point()
            return
        if action is MenuAction.CREATE_SEGMENT:
            self._create_segment()
            return
        if action is MenuAction.CREATE_CIRCLE:
            self._create_circle()
            return
        if action is MenuAction.CREATE_SQUARE:
            self._create_square()
            return
        if action is MenuAction.LIST_SHAPES:
            self._view.render_shapes(self._service.list_shapes())
            return
        if action is MenuAction.DELETE_SHAPE:
            self._delete_shape()
            return
        if action is MenuAction.HELP:
            self._view.render_help()
            return

    def _create_point(self) -> None:
        x = self._menu.ask_float("x")
        y = self._menu.ask_float("y")
        shape = self._service.create_point(x=x, y=y)
        self._view.success(f"Created {shape.shape_type} #{shape.id}: {shape.summary()}")

    def _create_segment(self) -> None:
        x1 = self._menu.ask_float("x1")
        y1 = self._menu.ask_float("y1")
        x2 = self._menu.ask_float("x2")
        y2 = self._menu.ask_float("y2")
        shape = self._service.create_segment(x1=x1, y1=y1, x2=x2, y2=y2)
        self._view.success(f"Created {shape.shape_type} #{shape.id}: {shape.summary()}")

    def _create_circle(self) -> None:
        center_x = self._menu.ask_float("center x")
        center_y = self._menu.ask_float("center y")
        radius = self._menu.ask_float("radius")
        shape = self._service.create_circle(center_x=center_x, center_y=center_y, radius=radius)
        self._view.success(f"Created {shape.shape_type} #{shape.id}: {shape.summary()}")

    def _create_square(self) -> None:
        x = self._menu.ask_float("origin x")
        y = self._menu.ask_float("origin y")
        side = self._menu.ask_float("side")
        shape = self._service.create_square(x=x, y=y, side=side)
        self._view.success(f"Created {shape.shape_type} #{shape.id}: {shape.summary()}")

    def _delete_shape(self) -> None:
        shapes = self._service.list_shapes()
        if not shapes:
            self._view.info("There are no shapes to delete.")
            return

        shape_id = self._menu.choose_shape_id([shape.id for shape in shapes])
        if shape_id is None:
            self._view.info("Deletion cancelled.")
            return

        deleted_shape = self._service.delete_shape(shape_id)
        self._view.success(f"Deleted {deleted_shape.shape_type} #{deleted_shape.id}.")