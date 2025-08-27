# Beam Analysis

Beam Analysis is a lightweight Python package for structural beam analysis.

### Example - Cantilever Beam

    from pybeam import members

    length = 5  # m
    resolution = 1000  # points
    load = 50  # N
    load_position = 5  # m

    # create generic loadable member
    loadable = members.Loadable(length, resolution)

    # add load 
    loadable.add_shear_point_force(load, load_position/length)  # relative position

    # reaction loads (no automated solver yet)
    loadable.add_shear_point_force(-load, 0)
    loadable.add_point_moment(-load*length, 0)

    loadable.plot()



Sign convention: positive shear loads downwards.

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

