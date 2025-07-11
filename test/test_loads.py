import numpy as np
import pytest

from pybeam.loads import PointForce

def test_point_load_distribution():
    magnitude = 10.0  # Newtons
    normalized_position = 0.5 
    point_load = PointForce(magnitude, normalized_position)

    # Define a positions array
    length = 2.0  # meters
    num_points = 100
    positions = np.linspace(0, length, num_points)

    distribution = point_load.load_distribution(positions)

    # all zeros except one non-zero entry equal to magnitude
    non_zero_indices = np.nonzero(distribution)[0]

    # There should be exactly 1 non-zero entry
    assert len(non_zero_indices) == 1

    index = non_zero_indices[0]

    # The value should match the magnitude
    assert distribution[index] == pytest.approx(magnitude)

    # The position should be close to the normalized position * length
    expected_position = normalized_position * length
    actual_position = positions[index]
    assert actual_position == pytest.approx(expected_position, abs=length/num_points)

