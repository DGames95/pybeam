# Beam Analysis

Beam Analysis is a lightweight Python package for structural beam analysis.

### Example

    from pybeam import loads, loading_case, analyze, visualizers

    # supported beam
    point_force = loads.PointForce(20, 0)
    point_force_2 = loads.PointForce(20, 1)
    point_force_3 = loads.PointForce(-40, 0.5)

    # define shear loads on a beam length 1
    supported_beam = loading_case.LoadingCase( 1, 1000, [], [point_force, point_force_2, point_force_3], [], [], "Supported Beam")

    analyzer = analyze.BeamAnalyzer(supported_beam)

    analyzer.visualize(visualizers.MatplotlibVisualizer())


Sign convention: positive shear loads upwards, may be inverted to standard civil beam analysis.

### Use
(windows)

clone repo

    python -m venv ./venv
    ./venv/Scripts/Activate.ps1

    pip install -r requirements.txt
    

test:
    pip install -r requirements-dev.txt
    python -m pytest .\test\

    coverage run -m pytest
    coverage report -m

#### build

    python -m build

whl file in dist/

