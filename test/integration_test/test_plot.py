import pytest
from pybeam import analyze, visualizers, loading_case, loads

@pytest.mark.skip(reason="Manual Test")
def test_plotting_point_load():
    point_force = loads.PointForce(20, 0)
    point_force_2 = loads.PointForce(20, 1)
    point_force_3 = loads.PointForce(-40, 0.5)

    supported_beam = loading_case.LoadingCase( 1, 1000, [], [point_force, point_force_2, point_force_3], [], [], "Supported Beam")

    analyzer = analyze.BeamAnalyzer(supported_beam)

    analyzer.visualize(visualizers.MatplotlibVisualizer())

if __name__=="__main__":
    test_plotting_point_load()