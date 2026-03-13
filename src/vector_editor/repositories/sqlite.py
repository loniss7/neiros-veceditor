from __future__ import annotations

import sqlite3
from pathlib import Path

from vector_editor.domain.base import Shape
from vector_editor.domain.shapes import Circle, Oval, Point, Rectangle, Segment, Square


class SQLiteShapeRepository:
    def __init__(self, db_path: str | Path = "vector_editor.db") -> None:
        self._db_path = Path(db_path)
        self._connection = sqlite3.connect(self._db_path)
        self._connection.row_factory = sqlite3.Row
        self._init_db()

    def next_id(self) -> int:
        row = self._connection.execute(
            "SELECT COALESCE(MAX(id), 0) + 1 AS next_id FROM shapes"
        ).fetchone()
        return int(row["next_id"])

    def add(self, shape: Shape) -> Shape:
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO shapes (
                    id, type, x, y, x1, y1, x2, y2, center_x, center_y,
                    radius, side, radius_x, radius_y, width, height
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._shape_to_row(shape),
            )
        return shape

    def list_all(self) -> list[Shape]:
        rows = self._connection.execute(
            "SELECT * FROM shapes ORDER BY id ASC"
        ).fetchall()
        return [self._row_to_shape(row) for row in rows]

    def exists(self, shape_id: int) -> bool:
        row = self._connection.execute(
            "SELECT 1 FROM shapes WHERE id = ?",
            (shape_id,),
        ).fetchone()
        return row is not None

    def remove(self, shape_id: int) -> Shape:
        row = self._connection.execute(
            "SELECT * FROM shapes WHERE id = ?",
            (shape_id,),
        ).fetchone()
        if row is None:
            raise KeyError(shape_id)

        shape = self._row_to_shape(row)

        with self._connection:
            self._connection.execute(
                "DELETE FROM shapes WHERE id = ?",
                (shape_id,),
            )
        return shape

    def close(self) -> None:
        self._connection.close()

    def _init_db(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS shapes (
                    id INTEGER PRIMARY KEY,
                    type TEXT NOT NULL,
                    x REAL,
                    y REAL,
                    x1 REAL,
                    y1 REAL,
                    x2 REAL,
                    y2 REAL,
                    center_x REAL,
                    center_y REAL,
                    radius REAL,
                    side REAL,
                    radius_x REAL,
                    radius_y REAL,
                    width REAL,
                    height REAL
                )
                """
            )

        # Миграция для старых БД: добавляем отсутствующие колонки
        required_columns = {
            "x": "REAL",
            "y": "REAL",
            "x1": "REAL",
            "y1": "REAL",
            "x2": "REAL",
            "y2": "REAL",
            "center_x": "REAL",
            "center_y": "REAL",
            "radius": "REAL",
            "side": "REAL",
            "radius_x": "REAL",
            "radius_y": "REAL",
            "width": "REAL",
            "height": "REAL",
        }

        existing_columns = {
            row["name"]
            for row in self._connection.execute("PRAGMA table_info(shapes)").fetchall()
        }

        missing_columns = [
            (name, col_type)
            for name, col_type in required_columns.items()
            if name not in existing_columns
        ]

        if missing_columns:
            with self._connection:
                for name, col_type in missing_columns:
                    self._connection.execute(
                        f"ALTER TABLE shapes ADD COLUMN {name} {col_type}"
                    )

    @staticmethod
    def _shape_to_row(shape: Shape) -> tuple:
        if isinstance(shape, Point):
            return (
                shape.id,
                "Point",
                shape.x,
                shape.y,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
        if isinstance(shape, Segment):
            return (
                shape.id,
                "Segment",
                None,
                None,
                shape.x1,
                shape.y1,
                shape.x2,
                shape.y2,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
        if isinstance(shape, Circle):
            return (
                shape.id,
                "Circle",
                None,
                None,
                None,
                None,
                None,
                None,
                shape.center_x,
                shape.center_y,
                shape.radius,
                None,
                None,
                None,
                None,
                None,
            )
        if isinstance(shape, Square):
            return (
                shape.id,
                "Square",
                shape.x,
                shape.y,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                shape.side,
                None,
                None,
                None,
                None,
            )
        if isinstance(shape, Oval):
            return (
                shape.id,
                "Oval",
                None,
                None,
                None,
                None,
                None,
                None,
                shape.center_x,
                shape.center_y,
                None,
                None,
                shape.radius_x,
                shape.radius_y,
                None,
                None,
            )
        if isinstance(shape, Rectangle):
            return (
                shape.id,
                "Rectangle",
                shape.x,
                shape.y,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                shape.width,
                shape.height,
            )
        raise ValueError(f"Unsupported shape type: {type(shape).__name__}")

    @staticmethod
    def _row_to_shape(row: sqlite3.Row) -> Shape:
        shape_type = row["type"]

        if shape_type == "Point":
            return Point(id=row["id"], x=row["x"], y=row["y"])
        if shape_type == "Segment":
            return Segment(
                id=row["id"],
                x1=row["x1"],
                y1=row["y1"],
                x2=row["x2"],
                y2=row["y2"],
            )
        if shape_type == "Circle":
            return Circle(
                id=row["id"],
                center_x=row["center_x"],
                center_y=row["center_y"],
                radius=row["radius"],
            )
        if shape_type == "Square":
            return Square(
                id=row["id"],
                x=row["x"],
                y=row["y"],
                side=row["side"],
            )
        if shape_type == "Oval":
            return Oval(
                id=row["id"],
                center_x=row["center_x"],
                center_y=row["center_y"],
                radius_x=row["radius_x"],
                radius_y=row["radius_y"],
            )
        if shape_type == "Rectangle":
            return Rectangle(
                id=row["id"],
                x=row["x"],
                y=row["y"],
                width=row["width"],
                height=row["height"],
            )

        raise ValueError(f"Unknown shape type: {shape_type}")