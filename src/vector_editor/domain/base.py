from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class Shape(ABC):
    id: int

    @property
    @abstractmethod
    def shape_type(self) -> str:
        """Human-readable shape type."""

    @abstractmethod
    def summary(self) -> str:
        """Compact description for CLI output."""