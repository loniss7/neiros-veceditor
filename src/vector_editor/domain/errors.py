class VectorEditorError(Exception):
    """Base exception for the application."""


class ValidationError(VectorEditorError):
    """Raised when input data is invalid."""


class ShapeNotFoundError(VectorEditorError):
    """Raised when a shape cannot be found by its identifier."""
