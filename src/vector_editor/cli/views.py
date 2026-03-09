from __future__ import annotations

from collections.abc import Sequence

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from vector_editor.domain.base import Shape


class RichCLIView:
    def __init__(self) -> None:
        self.console = Console()

    def render_header(self) -> None:
        self.console.print(
            Panel.fit(
                "[bold cyan]Vector Editor CLI[/bold cyan]\n"
                "[dim]Questionary + Rich presentation layer, ready for Textual adapter[/dim]",
                border_style="blue",
            )
        )

    def render_help(self) -> None:
        self.console.print(
            Panel(
                "[bold]Supported shapes:[/bold] Point, Segment, Circle, Square\n"
                "[bold]Operations:[/bold] Create, Delete, List, Help, Exit",
                title="Help",
                border_style="green",
            )
        )

    def render_shapes(self, shapes: Sequence[Shape]) -> None:
        if not shapes:
            self.console.print("[yellow]No shapes have been created yet.[/yellow]")
            return

        table = Table(title="Created shapes", header_style="bold magenta")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Type", style="green")
        table.add_column("Parameters", style="white")

        for shape in shapes:
            table.add_row(str(shape.id), shape.shape_type, shape.summary())

        self.console.print(table)

    def success(self, message: str) -> None:
        self.console.print(f"[bold green]OK:[/bold green] {message}")

    def error(self, message: str) -> None:
        self.console.print(f"[bold red]Error:[/bold red] {message}")

    def info(self, message: str) -> None:
        self.console.print(f"[bold blue]Info:[/bold blue] {message}")
