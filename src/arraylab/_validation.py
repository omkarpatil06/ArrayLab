"""Shared boundary checks; no silent reshaping of scientific data."""

import numpy as np
from numpy.typing import ArrayLike, NDArray


def array(value: ArrayLike, ndim: int, name: str) -> NDArray:
    """Require a nonempty finite numeric array of the specified rank."""
    result = np.asarray(value)
    if result.ndim != ndim or result.size == 0:
        raise ValueError(f"{name} must be a nonempty {ndim}-D array")
    if not np.issubdtype(result.dtype, np.number) or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain finite numbers")
    return result


def positive(value: float, name: str) -> None:
    """Require a positive finite real scalar."""
    if not np.isscalar(value) or not np.isreal(value) or not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")


def count(value: int, name: str) -> None:
    """Require a positive integer, excluding booleans."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
