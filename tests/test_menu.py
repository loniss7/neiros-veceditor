import questionary

from vector_editor.cli.menu import MenuAction, QuestionaryMenu


class DummyPrompt:
    def __init__(self, value):
        self.value = value

    def ask(self):
        return self.value


def test_choose_action(monkeypatch):
    monkeypatch.setattr(
        questionary,
        "select",
        lambda *args, **kwargs: DummyPrompt("Create point"),
    )

    menu = QuestionaryMenu()

    action = menu.choose_action()

    assert action == MenuAction.CREATE_POINT


def test_choose_action_returns_exit_on_none(monkeypatch):
    monkeypatch.setattr(
        questionary,
        "select",
        lambda *args, **kwargs: DummyPrompt(None),
    )

    menu = QuestionaryMenu()

    action = menu.choose_action()

    assert action == MenuAction.EXIT


def test_ask_float(monkeypatch):
    monkeypatch.setattr(
        questionary,
        "text",
        lambda *args, **kwargs: DummyPrompt("12.5"),
    )

    menu = QuestionaryMenu()

    value = menu.ask_float("x")

    assert value == 12.5


def test_ask_float_raises_keyboard_interrupt_on_none(monkeypatch):
    monkeypatch.setattr(
        questionary,
        "text",
        lambda *args, **kwargs: DummyPrompt(None),
    )

    menu = QuestionaryMenu()

    try:
        menu.ask_float("x")
        assert False, "KeyboardInterrupt was not raised"
    except KeyboardInterrupt:
        assert True


def test_choose_shape_id(monkeypatch):
    monkeypatch.setattr(
        questionary,
        "select",
        lambda *args, **kwargs: DummyPrompt("2"),
    )

    menu = QuestionaryMenu()

    value = menu.choose_shape_id([1, 2, 3])

    assert value == 2


def test_choose_shape_id_returns_none_for_empty_list():
    menu = QuestionaryMenu()

    assert menu.choose_shape_id([]) is None


def test_validate_float_accepts_number():
    assert QuestionaryMenu._validate_float("123") is True
    assert QuestionaryMenu._validate_float("1.5") is True


def test_validate_float_rejects_bad_value():
    assert QuestionaryMenu._validate_float("abc") == "Enter a valid number."