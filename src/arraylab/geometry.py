"""Array coordinates in metres."""

import numpy as np
from numpy.typing import NDArray

from ._validation import count, positive


def ula(sensors: int, spacing_m: float) -> NDArray[np.float64]:
    """Return centred x coordinates, shape (M,), for a uniform linear array.

    One sensor is valid and is located at zero. Spacing must remain positive.
    """
    count(sensors, "sensors")
    positive(spacing_m, "spacing_m")
    return (np.arange(sensors, dtype=float) - (sensors - 1) / 2) * spacing_m
