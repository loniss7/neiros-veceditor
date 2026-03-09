from vector_editor import app


class DummyController:
    def __init__(self):
        self.ran = False

    def run(self):
        self.ran = True


def test_main_runs_controller(monkeypatch):
    controller = DummyController()

    monkeypatch.setattr(app, "InMemoryShapeRepository", lambda: object())
    monkeypatch.setattr(app, "ShapeService", lambda repository: object())
    monkeypatch.setattr(app, "RichCLIView", lambda: object())
    monkeypatch.setattr(app, "QuestionaryMenu", lambda: object())

    def fake_controller(service, view, menu):
        return controller

    monkeypatch.setattr(app, "CLIController", fake_controller)

    app.main()

    assert controller.ran is True