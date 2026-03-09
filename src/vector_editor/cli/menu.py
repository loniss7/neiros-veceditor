from __future__ import annotations

from enum import StrEnum

import questionary


class MenuAction(StrEnum):
    CREATE_POINT = "Create point"
    CREATE_SEGMENT = "Create segment"
    CREATE_CIRCLE = "Create circle"
    CREATE_SQUARE = "Create square"
    LIST_SHAPES = "List shapes"
    DELETE_SHAPE = "Delete shape"
    HELP = "Help"
    EXIT = "Exit"


class QuestionaryMenu:
    def choose_action(self) -> MenuAction:
        answer = questionary.select(
            "Choose an action:",
            choices=[action.value for action in MenuAction],
            use_indicator=True,
        ).ask()

        if answer is None:
            return MenuAction.EXIT

        return MenuAction(answer)

    def ask_float(self, label: str) -> float:
        raw_value = questionary.text(
            label,
            validate=lambda text: self._validate_float(text),
        ).ask()

        if raw_value is None:
            raise KeyboardInterrupt

        return float(raw_value)

    def choose_shape_id(self, available_ids: list[int]) -> int | None:
        if not available_ids:
            return None

        answer = questionary.select(
            "Choose shape id to delete:",
            choices=[str(shape_id) for shape_id in available_ids],
            use_indicator=True,
        ).ask()
        return int(answer) if answer is not None else None

    def pause(self) -> None:
        questionary.text("Press Enter to continue").ask()

    @staticmethod
    def _validate_float(text: str) -> bool | str:
        try:
            float(text)
        except ValueError:
            return "Enter a valid number."
        return True
