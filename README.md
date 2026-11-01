# ArrayLab

A Python workbench for experimenting with sensor arrays and beamforming.
Intended for students and engineers who want to compare numerical results with
signal-processing theory.

## What works today

- Uniform linear array geometry and narrowband plane-wave simulation.
- Conventional beamforming and spatial response plots.
- Reproducible white-noise experiments with a fixed random seed.
- Tests against analytical phase, null locations and array-gain predictions.

Built with Python 3.12+, NumPy and optional Matplotlib. Tests use pytest; code
checks use Ruff. The numerical package runs independently of any interface.

## Run

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,plot]'
pytest -q
python examples/conventional.py --output outputs
```

On Windows, activate with `.venv\Scripts\activate`.
The example writes a beam-pattern PNG, CSV data and experiment parameters in JSON.
For eight sensors, predicted white-noise SNR gain is 9.03 dB; the seeded example
measures approximately 8.99 dB.

## Model

Sensors lie along x. Angles are measured from broadside toward +x, in radians.
With the exp(+j omega t) convention, receive steering is
`a_m = exp(+j 2*pi*f*x_m*sin(theta)/c)`. Observations have shape
`(sensors, snapshots)` and beamformer output is `w.conj() @ X`.
See [mathematical assumptions and validation](docs/mathematics.md).

## Next

See [ROADMAP.md](ROADMAP.md): interference analysis, experiment export/reload,
an interactive interface, MVDR and MUSIC. These features are planned.

## Status and license

New independent project started on 1 November 2026, with the initial prototype
prepared using an AI coding assistant. No established users or releases yet.
All example data is synthetic; no thesis or employer source code was imported.
Licensed under [MIT](LICENSE).
