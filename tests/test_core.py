"""Validate against physical phase and closed-form/statistical predictions."""

import numpy as np
import pytest
from numpy.testing import assert_allclose

from arraylab import (
    apply_beamformer,
    complex_white_noise,
    conventional_weights,
    plane_wave,
    power_response,
    steering_vector,
    ula,
)


def test_geometry():
    assert_allclose(ula(4, 0.2), [-0.3, -0.1, 0.1, 0.3])
    assert_allclose(ula(1, 0.2), [0])


def test_independent_physical_phase_sign():
    # +30-degree source is lambda/4 closer to the sensor at x=lambda/2.
    # Earlier arrival with exp(+jwt) means a +pi/2 phase advance.
    assert_allclose(steering_vector([0, 0.5], np.pi / 6, 343), [1, 1j], atol=1e-14)
    assert_allclose(steering_vector([0, 0.5], -np.pi / 6, 343), [1, -1j], atol=1e-14)


@pytest.mark.parametrize("m", [1, 2, 8])
@pytest.mark.parametrize("look", [-0.7, 0, 0.4])
def test_unity_and_recovery(m, look):
    a = steering_vector(ula(m, 0.1), look, 1000)
    w = conventional_weights(a)
    s = np.array([1 + 2j, -2j, 0.5])
    assert_allclose(np.vdot(w, a), 1, atol=1e-14)
    assert_allclose(apply_beamformer(w, plane_wave(a, s)), s, atol=1e-14)
    assert power_response(w, a) == pytest.approx(1)


def test_closed_form():
    m, d, look = 7, 0.45, 0.21
    w = conventional_weights(steering_vector(ula(m, d), look, 343))
    for theta in np.linspace(-np.pi / 2, np.pi / 2, 101):
        psi = 2 * np.pi * d * (np.sin(theta) - np.sin(look))
        expected = (np.sinc(m * psi / (2 * np.pi)) / np.sinc(psi / (2 * np.pi))) ** 2
        assert power_response(w, steering_vector(ula(m, d), theta, 343)) == pytest.approx(
            expected, abs=2e-14
        )


def test_null_and_alias():
    w = np.ones(8) / 8
    assert power_response(w, steering_vector(ula(8, 0.5), np.arcsin(0.25), 343)) < 1e-28
    assert power_response(w, steering_vector(ula(8, 1), np.pi / 2, 343)) == pytest.approx(1)


def test_translation():
    positions = ula(5, 0.1)
    a = steering_vector(positions, 0.4, 1000)
    shifted = steering_vector(positions + 2.1, 0.4, 1000)
    assert_allclose(shifted, a * np.exp(2j * np.pi * 1000 / 343 * 2.1 * np.sin(0.4)), atol=1e-13)


def test_noise_statistics_and_gain():
    m, n, power = 8, 100000, 2
    v = complex_white_noise(m, n, power, np.random.default_rng(73))
    assert_allclose(v @ v.conj().T / n, power * np.eye(m), atol=0.025, rtol=0)
    assert np.mean(v.real**2) == pytest.approx(power / 2, rel=0.01)
    assert np.mean(v.imag**2) == pytest.approx(power / 2, rel=0.01)
    w = conventional_weights(steering_vector(ula(m, 0.1), 0.3, 1000))
    assert np.vdot(w, w).real == pytest.approx(1 / m)
    assert np.mean(abs(apply_beamformer(w, v)) ** 2) == pytest.approx(power / m, rel=0.02)


def test_seed_zero_and_linearity():
    v = complex_white_noise(2, 30, 1, np.random.default_rng(42))
    assert_allclose(v, complex_white_noise(2, 30, 1, np.random.default_rng(42)))
    assert_allclose(complex_white_noise(2, 30, 0, np.random.default_rng(42)), 0)
    x = plane_wave([1, 1j], np.ones(30))
    w = conventional_weights([1, 1j])
    assert_allclose(apply_beamformer(w, x + v), apply_beamformer(w, x) + apply_beamformer(w, v))


@pytest.mark.parametrize("m,d", [(0, 1), (True, 1), (2.5, 1), (2, 0), (2, np.nan)])
def test_invalid_geometry(m, d):
    with pytest.raises(ValueError):
        ula(m, d)


@pytest.mark.parametrize(
    "theta,f,c",
    [(np.nan, 1, 343), (2, 1, 343), (0, 0, 343), (0, 1, -1), (0, np.inf, 343), (0, 1j, 343)],
)
def test_invalid_model(theta, f, c):
    with pytest.raises(ValueError):
        steering_vector([0, 1], theta, f, c)


def test_invalid_shapes_and_values():
    for positions in ([], [[0, 1]], [0, np.inf], [0, 1j]):
        with pytest.raises(ValueError):
            steering_vector(positions, 0, 1000)
    with pytest.raises(ValueError):
        conventional_weights([1, 2])
    with pytest.raises(ValueError):
        apply_beamformer([1, 1], np.ones((3, 10)))
    with pytest.raises(ValueError):
        apply_beamformer([1], [1])
    with pytest.raises(ValueError):
        power_response([1], [1, 1])
    with pytest.raises(ValueError):
        plane_wave([1], [])
    with pytest.raises(ValueError):
        complex_white_noise(2, 4, -1, np.random.default_rng(0))
