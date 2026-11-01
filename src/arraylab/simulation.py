"""Component-level simulation: keep desired, interference and noise separate."""

import numpy as np
from numpy.typing import ArrayLike, NDArray

from ._validation import array, count


def plane_wave(steering: ArrayLike, signal: ArrayLike) -> NDArray[np.complex128]:
    """Form a s^T with shape (M, N); signal is a complex-envelope sequence."""
    a = array(steering, 1, "steering")
    s = array(signal, 1, "signal")
    return np.asarray(a[:, None] * s[None, :], dtype=np.complex128)


def complex_white_noise(
    sensors: int, snapshots: int, power: float, rng: np.random.Generator
) -> NDArray[np.complex128]:
    """Independent circular complex Gaussian noise with E|v_m[n]|^2=power.

    The caller owns the generator. Zero power is valid; negative/nonfinite is not.
    """
    count(sensors, "sensors")
    count(snapshots, "snapshots")
    if not np.isscalar(power) or not np.isreal(power) or not np.isfinite(power) or power < 0:
        raise ValueError("power must be nonnegative and finite")
    shape = (sensors, snapshots)
    return np.sqrt(power / 2) * (rng.standard_normal(shape) + 1j * rng.standard_normal(shape))
