"""Far-field narrowband receive steering; see docs/mathematics.md."""

import numpy as np
from numpy.typing import ArrayLike, NDArray

from ._validation import array, positive


def steering_vector(
    positions_m: ArrayLike, angle_rad: float, frequency_hz: float, sound_speed_m_s: float = 343.0
) -> NDArray[np.complex128]:
    """Return shape (M,) receive phases exp(+j 2 pi f x sin(theta)/c).

    Sensors lie along +x. Zero angle points toward a source on +y; positive
    angles turn toward +x. Input angles are radians in [-pi/2, pi/2].
    The source-bearing vector opposes the propagation direction.
    """
    positions = array(positions_m, 1, "positions_m")
    if np.iscomplexobj(positions):
        raise ValueError("positions_m must be real")
    positive(frequency_hz, "frequency_hz")
    positive(sound_speed_m_s, "sound_speed_m_s")
    if (
        not np.isscalar(angle_rad)
        or not np.isreal(angle_rad)
        or not np.isfinite(angle_rad)
        or abs(angle_rad) > np.pi / 2
    ):
        raise ValueError("angle_rad must be finite and in [-pi/2, pi/2]")
    return np.exp(2j * np.pi * frequency_hz / sound_speed_m_s * positions * np.sin(angle_rad))
