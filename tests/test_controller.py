from vector_editor.cli.controller import CLIController
from vector_editor.cli.menu import MenuAction
from vector_editor.domain.errors import ShapeNotFoundError, ValidationError
from vector_editor.domain.shapes import Point


class DummyMenu:
    def __init__(self, actions, float_values=None, shape_id=None, raises=None):
        self.actions = list(actions)
        self.float_values = list(float_values or [])
        self.shape_id = shape_id
        self.raises = raises
        self.float_labels = []

    def choose_action(self):
        if self.raises is not None:
            raise self.raises
        return self.actions.pop(0)

    def ask_float(self, label):
        self.float_labels.append(label)
        return self.float_values.pop(0)

    def choose_shape_id(self, available_ids):
        self.available_ids = available_ids
        return self.shape_id


class DummyView:
    def __init__(self):
        self.header_calls = 0
        self.help_calls = 0
        self.rendered_shapes = None
        self.success_messages = []
        self.info_messages = []
        self.error_messages = []

    def render_header(self):
        self.header_calls += 1

    def render_help(self):
        self.help_calls += 1

    def render_shapes(self, shapes):
        self.rendered_shapes = list(shapes)

    def success(self, message):
        self.success_messages.append(message)

    def info(self, message):
        self.info_messages.append(message)

    def error(self, message):
        self.error_messages.append(message)


def test_list_shapes(service):
    service.create_point(1, 2)
    menu = DummyMenu([MenuAction.LIST_SHAPES, MenuAction.EXIT])
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert view.header_calls == 1
    assert view.help_calls == 1
    assert len(view.rendered_shapes) == 1
    assert view.info_messages[-1] == "Goodbye."


def test_exit(service):
    menu = DummyMenu([MenuAction.EXIT])
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert view.header_calls == 1
    assert view.help_calls == 1
    assert view.info_messages == ["Goodbye."]


def test_create_point(service):
    menu = DummyMenu([MenuAction.CREATE_POINT, MenuAction.EXIT], float_values=[10, 20])
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert menu.float_labels == ["x", "y"]
    assert len(service.list_shapes()) == 1
    assert "Created Point #1: x=10, y=20" in view.success_messages[0]


def test_create_circle(service):
    menu = DummyMenu(
        [MenuAction.CREATE_CIRCLE, MenuAction.EXIT],
        float_values=[5, 6, 7],
    )
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert menu.float_labels == ["center x", "center y", "radius"]
    assert "Created Circle #1: center=(5, 6), radius=7" in view.success_messages[0]


def test_delete_shape(service):
    shape = service.create_point(1, 2)
    menu = DummyMenu([MenuAction.DELETE_SHAPE, MenuAction.EXIT], shape_id=shape.id)
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert menu.available_ids == [shape.id]
    assert service.list_shapes() == []
    assert view.success_messages[0] == f"Deleted Point #{shape.id}."


def test_delete_shape_when_empty(service):
    menu = DummyMenu([MenuAction.DELETE_SHAPE, MenuAction.EXIT])
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert view.info_messages[0] == "There are no shapes to delete."
    assert view.info_messages[-1] == "Goodbye."


def test_delete_shape_cancelled(service):
    service.create_point(1, 2)
    menu = DummyMenu([MenuAction.DELETE_SHAPE, MenuAction.EXIT], shape_id=None)
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert view.info_messages[0] == "Deletion cancelled."
    assert len(service.list_shapes()) == 1


def test_help_action(service):
    menu = DummyMenu([MenuAction.HELP, MenuAction.EXIT])
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert view.help_calls == 2


def test_keyboard_interrupt_is_handled(service):
    menu = DummyMenu([], raises=KeyboardInterrupt())
    view = DummyView()

    controller = CLIController(service, view, menu)

    # Break loop after one handled exception and one exit
    def choose_action_sequence():
        if not hasattr(menu, "_called"):
            menu._called = True
            raise KeyboardInterrupt()
        return MenuAction.EXIT

    menu.choose_action = choose_action_sequence

    controller.run()

    assert view.info_messages[0] == "Operation cancelled by user."
    assert view.info_messages[-1] == "Goodbye."


def test_validation_error_is_handled(service):
    menu = DummyMenu([MenuAction.CREATE_CIRCLE, MenuAction.EXIT], float_values=[0, 0, 0])
    view = DummyView()

    controller = CLIController(service, view, menu)
    controller.run()

    assert view.error_messages[0] == "Radius must be greater than zero."
    assert view.info_messages[-1] == "Goodbye."


def test_shape_not_found_error_is_handled(service):
    menu = DummyMenu([MenuAction.DELETE_SHAPE, MenuAction.EXIT], shape_id=999)
    view = DummyView()

    service.create_point(1, 2)

    controller = CLIController(service, view, menu)
    controller.run()

    assert view.error_messages[0] == "Shape with id=999 was not found."
    assert view.info_messages[-1] == "Goodbye."