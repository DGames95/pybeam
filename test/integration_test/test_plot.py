import pytest
import pybeam
from pybeam import analyze, visualizers, loading_case, loads

@pytest.mark.skip(reason="Manual Test, check that plot is shown correctly")
def test_plotting_point_load():
    point_force = loads.PointForce(20, 0)
    point_force_2 = loads.PointForce(20, 1)
    point_force_3 = loads.PointForce(-40, 0.5)

    supported_beam = loading_case.LoadingCase( 1, 1000, [], [point_force, point_force_2, point_force_3], [], [], "Supported Beam")

    analyzer = analyze.BeamAnalyzer(supported_beam)

    analyzer.visualize(visualizers.MatplotlibVisualizer())

@pytest.mark.skip(reason="Manual Test, check that plot is saved in temp directory")
def test_saving_plot_member():
    profile1 = pybeam.profiles.IBeamProfile(30, 20, 0.01, 0.01)

    material1 = pybeam.materials.Steel()

    member1 = pybeam.members.UniformMember(5, profile1, material1)

    member1.add_shear_load(10, 0.5)

    member1.plot()

    member1.save_plot("test1")

@pytest.mark.skip(reason="Manual Test, check that plot is created")
def test_plot_loadable():
    member1 = pybeam.members.Loadable(5, 1000)

    member1.add_shear_load(10, 0.5)

    member1.plot()

if __name__=="__main__":
    test_plotting_point_load()