"""Conventional narrowband beamforming without plotting or simulator dependencies."""

import numpy as np
from numpy.typing import ArrayLike, NDArray

from ._validation import array


def conventional_weights(steering: ArrayLike) -> NDArray[np.complex128]:
    """Return a/M for a unit-magnitude receive steering vector, shape (M,)."""
    a = array(steering, 1, "steering")
    if not np.allclose(np.abs(a), 1.0, rtol=0, atol=1e-12):
        raise ValueError("steering must have unit-magnitude elements")
    return np.asarray(a / a.size, dtype=np.complex128)


def apply_beamformer(weights: ArrayLike, observations: ArrayLike) -> NDArray[np.complex128]:
    """Compute w^H X; X has shape (M, N), output shape (N,)."""
    w = array(weights, 1, "weights")
    x = array(observations, 2, "observations")
    if x.shape[0] != w.size:
        raise ValueError("weights and observations must have the same sensor count")
    return np.asarray(w.conj() @ x, dtype=np.complex128)


def power_response(weights: ArrayLike, steering: ArrayLike) -> float:
    """Return absolute |w^H a|^2, without normalization to the plotted maximum."""
    w = array(weights, 1, "weights")
    a = array(steering, 1, "steering")
    if w.shape != a.shape:
        raise ValueError("weights and steering must have the same shape")
    return float(abs(np.vdot(w, a)) ** 2)
