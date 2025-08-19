import pytest

from pybeam import members, profiles, materials

def test_plotting_point_load():
    # get a moment of area of the profile.
    profile1 = profiles.IBeamProfile(30, 20, 0.01, 0.01)

    # get a material class with different properties.
    material1 = materials.Steel()

    # create beam with length 5m, I of this or a profile
    member1 = members.UniformMember(5, profile1, material1)

    assert member1.get_weight() == 5 * profile1.get_area() * material1.density