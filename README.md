# PyBeam – Structural Beam Analysis in Python

![Project Status: Alpha](https://img.shields.io/badge/status-alpha-orange)
![PyPI](https://img.shields.io/pypi/v/pybeam-structural)
![License](https://img.shields.io/github/license/dgames95/pybeam)
![Docs](https://img.shields.io/readthedocs/pybeam-structural)

**PyBeam** is a lightweight, Python-based library for analyzing beams. v0.1.0 supports creating internal stress diagrams

## Table of Contents

- [Installation](#installation)
- [Quick Example](#quick-example)
- [Sign Conventions](#sign-conventions)
- [Testing](#testing)
- [Build](#build)
- [Documentation](#documentation)
- [License](#license)

## Installation

Install via pip:

```bash
pip install pybeam-structural
````

## Quick Example – Cantilever Beam with Point Load

```python
from pybeam import members

# Define beam properties
length = 5  # meters
resolution = 1000

# Define load
load = 50  # N
load_position = 5  # meters from fixed end

# Create beam object
beam = members.Loadable(length, resolution)

# Apply point load (as fraction of beam length)
beam.add_shear_point_force(load, load_position / length)

# Manually add support reactions
beam.add_shear_point_force(-load, 0)            # Fixed end vertical reaction
beam.add_point_moment(-load * length, 0)        # Fixed end moment

# Plot shear and moment diagrams
beam.plot()
```

## Sign Conventions

* Positive **shear force**: acts **downward**
* Positive **moment**: causes **sagging** (concave up)

## Testing and Development

Install dev dependencies into a venv:

```bash
python3 -m venv ./venv
chmod +x ./venv/bin/activate
./venv/bin/activate
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest
```

Run with coverage:

```bash
coverage run -m pytest
coverage report -m
```

## Build

Build the package (creates `.whl` in `dist/`):

```bash
python -m build
```

## Documentation
[https://pybeam-structural.readthedocs.io/en/latest/](https://pybeam-structural.readthedocs.io/en/latest/)

Generated via sphinx, see [docs](./docs/README.md)


## License

MIT License – see [LICENSE](./LICENSE)


