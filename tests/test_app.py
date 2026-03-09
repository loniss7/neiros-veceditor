from vector_editor import app


class DummyController:
    def __init__(self):
        self.ran = False

    def run(self):
        self.ran = True


def test_build_application_returns_controller(monkeypatch):
    controller = DummyController()

    monkeypatch.setattr(app, "SQLiteShapeRepository", lambda: object())
    monkeypatch.setattr(app, "ShapeService", lambda repository: object())
    monkeypatch.setattr(app, "RichCLIView", lambda: object())
    monkeypatch.setattr(app, "QuestionaryMenu", lambda: object())
    monkeypatch.setattr(app, "CLIController", lambda service, view, menu: controller)

    result = app.build_application()

    assert result is controller


def test_main_runs_controller(monkeypatch):
    controller = DummyController()

    monkeypatch.setattr(app, "build_application", lambda: controller)

    app.main()

    assert controller.ran is True