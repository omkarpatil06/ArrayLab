"""Run after installing: python examples/conventional.py --output outputs."""

import argparse
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from arraylab import (
    apply_beamformer,
    complex_white_noise,
    conventional_weights,
    plane_wave,
    power_response,
    steering_vector,
    ula,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    seed, m, n, f, c, noise_power = 20261101, 8, 65536, 1000.0, 343.0, 1.0
    theta = np.deg2rad(20.0)
    positions = ula(m, c / f / 2)
    a = steering_vector(positions, theta, f, c)
    w = conventional_weights(a)
    desired = plane_wave(a, np.ones(n, dtype=complex))
    noise = complex_white_noise(m, n, noise_power, np.random.default_rng(seed))
    y = apply_beamformer(w, desired + noise)
    output_noise = apply_beamformer(w, noise)
    measured_gain_db = float(10 * np.log10(noise_power / np.mean(abs(output_noise) ** 2)))
    assert abs(measured_gain_db - 10 * np.log10(m)) < 0.15
    assert np.allclose(y, apply_beamformer(w, desired) + output_noise)
    degrees = np.linspace(-90, 90, 721)
    response = np.array(
        [power_response(w, steering_vector(positions, np.deg2rad(t), f, c)) for t in degrees]
    )
    np.savetxt(
        args.output / "pattern.csv",
        np.column_stack((degrees, response)),
        delimiter=",",
        header="angle_deg,power_gain",
        comments="",
    )
    fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
    ax.plot(degrees, 10 * np.log10(np.maximum(response, 1e-6)))
    ax.axvline(20, color="teal", linestyle="--", label="Look direction: 20 degrees")
    ax.set(
        xlabel="Source bearing from broadside (degrees)",
        ylabel="Absolute power gain (dB)",
        ylim=(-60, 1),
        xlim=(-90, 90),
        title="8 sensors, half-wavelength spacing",
    )
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig(args.output / "pattern.png", dpi=160)
    plt.close(fig)
    report = dict(
        seed=seed,
        sensors=m,
        snapshots=n,
        frequency_hz=f,
        sound_speed_m_s=c,
        spacing_m=c / f / 2,
        look_angle_deg=20,
        noise_power=noise_power,
        measured_snr_gain_db=measured_gain_db,
        predicted_snr_gain_db=float(10 * np.log10(m)),
        python=platform.python_version(),
        numpy=np.__version__,
        matplotlib=matplotlib.__version__,
    )
    (args.output / "experiment.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
