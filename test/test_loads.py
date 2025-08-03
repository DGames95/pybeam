import numpy as np
import pytest

from pybeam.loads import PointForce, UniformDistributedLoad

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

class TestUniformDistributedLoad:
    
    def test_init_valid_parameters(self):
        """Test initialization with valid parameters"""
        load = UniformDistributedLoad(100, 0.2, 0.8)
        
        assert load.w == 100
        assert load.start == 0.2
        assert load.end == 0.8
    
    def test_init_end_negative_raises_assertion_error(self):
        """Test that end < 0 raises AssertionError"""
        with pytest.raises(AssertionError):
            UniformDistributedLoad(100, 0, -0.1)
    
    def test_init_end_greater_than_one_raises_assertion_error(self):
        """Test that end > 1 raises AssertionError"""
        with pytest.raises(AssertionError):
            UniformDistributedLoad(100, 0.5, 1.1)
    
    def test_init_boundary_conditions(self):
        """Test initialization with boundary values (0 and 1)"""
        # Full span load
        load1 = UniformDistributedLoad(50, 0.0, 1.0)
        assert load1.start == 0.0 and load1.end == 1.0
        
        # Load starting at 0
        load2 = UniformDistributedLoad(50, 0.0, 0.5)
        assert load2.start == 0.0 and load2.end == 0.5
        
        # Load ending at 1
        load3 = UniformDistributedLoad(50, 0.5, 1.0)
        assert load3.start == 0.5 and load3.end == 1.0
    
    def test_load_distribution_full_span(self):
        """Test load_distribution for full span load"""
        load = UniformDistributedLoad(100, 0.0, 1.0)
        inputs = np.linspace(0, 1, 11) 
        
        result = load.load_distribution(inputs)
        dx = inputs[1] - inputs[0]  # 0.1
        expected = np.ones_like(inputs) * 100 * dx
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_load_distribution_partial_span(self):
        """Test load_distribution for partial span load"""
        load = UniformDistributedLoad(200, 0.2, 0.8)
        inputs = np.linspace(0, 1, 11)
        
        result = load.load_distribution(inputs)
        dx = inputs[1] - inputs[0]  # 0.1
        
        # Calculate expected indices
        x1 = int(np.round(0.2 * len(inputs)))  # 2
        x2 = int(np.round(0.8 * len(inputs)))  # 9
        
        expected = np.zeros_like(inputs)
        expected[x1:x2] = 200 * dx
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_load_distribution_small_span(self):
        """Test load_distribution for small span load"""
        load = UniformDistributedLoad(500, 0.45, 0.55)
        inputs = np.linspace(0, 1, 21)  # More points for better resolution
        
        result = load.load_distribution(inputs)
        dx = inputs[1] - inputs[0]  # 0.05
        
        # Calculate expected indices
        x1 = int(np.round(0.45 * len(inputs)))  # 9
        x2 = int(np.round(0.55 * len(inputs)))  # 12
        
        expected = np.zeros_like(inputs)
        expected[x1:x2] = 500 * dx
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_load_distribution_at_start_boundary(self):
        """Test load_distribution starting at 0"""
        load = UniformDistributedLoad(150, 0.0, 0.3)
        inputs = np.linspace(0, 1, 11)
        
        result = load.load_distribution(inputs)
        dx = inputs[1] - inputs[0]
        
        x1 = int(np.round(0.0 * len(inputs)))  # 0
        x2 = int(np.round(0.3 * len(inputs)))  # 3
        
        expected = np.zeros_like(inputs)
        expected[x1:x2] = 150 * dx
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_load_distribution_at_end_boundary(self):
        """Test load_distribution ending at 1"""
        load = UniformDistributedLoad(250, 0.7, 1.0)
        inputs = np.linspace(0, 1, 11)
        
        result = load.load_distribution(inputs)
        dx = inputs[1] - inputs[0]
        
        x1 = int(np.round(0.7 * len(inputs)))  # 8
        x2 = int(np.round(1.0 * len(inputs)))  # 11
        
        expected = np.zeros_like(inputs)
        expected[x1:x2] = 250 * dx
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_load_distribution_different_input_sizes(self):
        """Test load_distribution with different input array sizes"""
        load = UniformDistributedLoad(100, 0.25, 0.75)
        
        # Test with different array sizes
        for size in [5, 10, 20, 50, 101]:
            inputs = np.linspace(0, 1, size)
            result = load.load_distribution(inputs)
            
            # Should return array of same size
            assert len(result) == size
            
            # Should have non-zero values in the middle region
            dx = inputs[1] - inputs[0] if size > 1 else 1.0
            x1 = int(np.round(0.25 * size))
            x2 = int(np.round(0.75 * size))
            
            if x1 < x2:  # Only test if there's a valid range
                assert np.any(result[x1:x2] > 0), f"No load applied for size {size}"
    
    def test_load_distribution_negative_load(self):
        """Test load_distribution with negative load value"""
        load = UniformDistributedLoad(-100, 0.2, 0.8)
        inputs = np.linspace(0, 1, 11)
        
        result = load.load_distribution(inputs)
        dx = inputs[1] - inputs[0]
        
        x1 = int(np.round(0.2 * len(inputs)))
        x2 = int(np.round(0.8 * len(inputs)))
        
        expected = np.zeros_like(inputs)
        expected[x1:x2] = -100 * dx
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_load_distribution_zero_load(self):
        """Test load_distribution with zero load value"""
        load = UniformDistributedLoad(0, 0.2, 0.8)
        inputs = np.linspace(0, 1, 11)
        
        result = load.load_distribution(inputs)
        expected = np.zeros_like(inputs)
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_get_total_force_full_span(self):
        """Test get_total_force for full span load"""
        load = UniformDistributedLoad(100, 0.0, 1.0)
        length = 10.0
        
        result = load.get_total_force(length)
        expected = 100 * (1.0 - 0.0) * 10.0  # w * span * length = 1000
        
        assert result == expected
    
    def test_get_total_force_partial_span(self):
        """Test get_total_force for partial span load"""
        load = UniformDistributedLoad(200, 0.2, 0.8)
        length = 5.0
        
        result = load.get_total_force(length)
        expected = 200 * (0.8 - 0.2) * 5.0  # w * span * length = 600
        
        assert result == expected
    
    def test_get_total_force_negative_load(self):
        """Test get_total_force with negative load"""
        load = UniformDistributedLoad(-150, 0.3, 0.7)
        length = 4.0
        
        result = load.get_total_force(length)
        expected = -150 * (0.7 - 0.3) * 4.0  # w * span * length = -240
        
        assert result == expected
    
    def test_get_total_force_zero_load(self):
        """Test get_total_force with zero load"""
        load = UniformDistributedLoad(0, 0.2, 0.8)
        length = 10.0
        
        result = load.get_total_force(length)
        expected = 0
        
        assert result == expected
    
    def test_get_total_force_different_lengths(self):
        """Test get_total_force with different beam lengths"""
        load = UniformDistributedLoad(100, 0.25, 0.75)
        
        lengths = [1.0, 2.5, 5.0, 10.0, 20.0]
        for length in lengths:
            result = load.get_total_force(length)
            expected = 100 * (0.75 - 0.25) * length  # w * 0.5 * length
            
            assert result == expected, f"Failed for length {length}"
    
    def test_consistency_between_methods(self):
        """Test consistency between load_distribution and get_total_force"""
        load = UniformDistributedLoad(200, 0.2, 0.8)
        length = 1
        inputs = np.linspace(0, 1, 10001)  # High resolution for accuracy
        
        # Get total force from get_total_force method
        total_force_method = load.get_total_force(length)
        
        # Get total force by integrating load_distribution
        distribution = load.load_distribution(inputs)
        total_force_integration = np.sum(distribution)
        
        # They should be approximately equal
        np.testing.assert_almost_equal(total_force_integration, total_force_method, decimal=1)

if __name__ == "__main__":
    pytest.main([__file__])