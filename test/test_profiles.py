import pytest
import numpy as np
from pybeam.profiles import IBeamProfile

def test_ibeam_profile():
    # Create an instance of IBeamProfile
    ibeam = IBeamProfile(width=0.3, height=0.5, flange_thickness=0.02, web_thickness=0.01)

    # Test the area calculation
    expected_area = 0.3 * 0.02 * 2 + 0.01 * (0.5 - 0.02 * 2) 
    assert np.isclose(ibeam.get_area(), expected_area), "Area calculation is incorrect"

    # Test the moment of inertia calculation
    expected_moi = 7.727e-4  # hand calculation
    assert np.isclose(ibeam.get_area_moment_of_inertia(), expected_moi), "Moment of inertia calculation is incorrect"
