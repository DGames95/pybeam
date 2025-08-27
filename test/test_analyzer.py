import pytest
import numpy as np
from unittest.mock import Mock, patch
from pybeam.analyze import BeamAnalyzer
from pybeam.loading_case import LoadingCase
from pybeam.loads import Load


class TestBeamAnalyzer:
    
    @pytest.fixture
    def mock_load_case(self):
        """Create a mock LoadingCase for testing"""
        mock_case = Mock(spec=LoadingCase)
        mock_case.points = np.linspace(0, 1, 11)
        mock_case.length = 1.0
        mock_case.axial_loads = []
        mock_case.shear_loads = []
        mock_case.point_moments = []
        mock_case.torsional_loads = []
        return mock_case
    
    @pytest.fixture
    def analyzer(self, mock_load_case):
        """Create a BeamAnalyzer instance for testing"""
        return BeamAnalyzer(mock_load_case)
    
    def test_init(self, mock_load_case):
        """Test BeamAnalyzer initialization"""
        analyzer = BeamAnalyzer(mock_load_case)
        
        assert analyzer.case == mock_load_case
        assert np.array_equal(analyzer.points, mock_load_case.points)
        assert analyzer.length == mock_load_case.length
    
    def test_get_internal_axial_force_no_loads(self, analyzer):
        """Test get_internal_axial_force with no axial loads"""
        result = analyzer.get_internal_axial_force()
        expected = np.zeros_like(analyzer.points)
        
        np.testing.assert_array_equal(result, expected)
    
    def test_get_internal_axial_force_single_load(self, analyzer):
        """Test get_internal_axial_force with single axial load"""
        mock_load = Mock(spec=Load)
        mock_load.load_distribution.return_value = np.ones_like(analyzer.points) * 10
        analyzer.case.axial_loads = [mock_load]
        
        result = analyzer.get_internal_axial_force()
        expected = np.ones_like(analyzer.points) * 10
        
        np.testing.assert_array_equal(result, expected)
        mock_load.load_distribution.assert_called_once_with(analyzer.points)
    
    def test_get_internal_axial_force_multiple_loads(self, analyzer):
        """Test get_internal_axial_force with multiple axial loads"""
        mock_load1 = Mock(spec=Load)
        mock_load1.load_distribution.return_value = np.ones_like(analyzer.points) * 5
        
        mock_load2 = Mock(spec=Load)
        mock_load2.load_distribution.return_value = np.ones_like(analyzer.points) * 3
        
        analyzer.case.axial_loads = [mock_load1, mock_load2]
        
        result = analyzer.get_internal_axial_force()
        expected = np.ones_like(analyzer.points) * 8
        
        np.testing.assert_array_equal(result, expected)
    
    def test_get_shear_loads_no_loads(self, analyzer):
        """Test get_shear_loads with no shear loads"""
        result = analyzer.get_shear_loads()
        expected = np.zeros_like(analyzer.points)
        
        np.testing.assert_array_equal(result, expected)
    
    def test_get_shear_loads_single_load(self, analyzer):
        """Test get_shear_loads with single shear load"""
        mock_load = Mock(spec=Load)
        mock_load.load_distribution.return_value = np.ones_like(analyzer.points) * 15
        analyzer.case.shear_loads = [mock_load]
        
        result = analyzer.get_shear_loads()
        expected = np.ones_like(analyzer.points) * 15
        
        np.testing.assert_array_equal(result, expected)
        mock_load.load_distribution.assert_called_once_with(analyzer.points)
    
    def test_get_shear_loads_multiple_loads(self, analyzer):
        """Test get_shear_loads with multiple shear loads"""
        mock_load1 = Mock(spec=Load)
        mock_load1.load_distribution.return_value = np.ones_like(analyzer.points) * 7
        
        mock_load2 = Mock(spec=Load)
        mock_load2.load_distribution.return_value = np.ones_like(analyzer.points) * 2
        
        analyzer.case.shear_loads = [mock_load1, mock_load2]
        
        result = analyzer.get_shear_loads()
        expected = np.ones_like(analyzer.points) * 9
        
        np.testing.assert_array_equal(result, expected)
    
    def test_get_internal_shear(self, analyzer):
        """Test get_internal_shear calculation"""
        # Mock get_shear_loads to return a constant distribution
        with patch.object(analyzer, 'get_shear_loads') as mock_shear:
            mock_shear.return_value = np.ones_like(analyzer.points) * 5
            
            result = analyzer.get_internal_shear()
            expected = np.cumsum(np.ones_like(analyzer.points) * 5)
            
            np.testing.assert_array_equal(result, expected)
    
    def test_get_internal_moments_no_point_moments(self, analyzer):
        """Test get_internal_moments with no point moments"""
        # Mock get_internal_shear to return known values
        with patch.object(analyzer, 'get_internal_shear') as mock_shear:
            shear_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            mock_shear.return_value = shear_values
            
            result = analyzer.get_internal_moments()
            
            dx = analyzer.points[1] - analyzer.points[0]  # 0.1
            expected = np.cumsum(shear_values * dx)
            
            np.testing.assert_array_almost_equal(result, expected)
    
    def test_get_internal_torsion_no_loads(self, analyzer):
        """Test get_internal_torsion with no torsional loads"""
        result = analyzer.get_internal_torsion()
        expected = np.zeros_like(analyzer.points)
        
        np.testing.assert_array_equal(result, expected)
    
    def test_get_internal_torsion_single_load(self, analyzer):
        """Test get_internal_torsion with single torsional load"""
        mock_load = Mock(spec=Load)
        mock_load.load_distribution.return_value = np.ones_like(analyzer.points) * 12
        analyzer.case.torsional_loads = [mock_load]
        
        result = analyzer.get_internal_torsion()
        expected = np.ones_like(analyzer.points) * 12
        
        np.testing.assert_array_equal(result, expected)
        mock_load.load_distribution.assert_called_once_with(analyzer.points)
    
    def test_get_internal_torsion_multiple_loads(self, analyzer):
        """Test get_internal_torsion with multiple torsional loads"""
        mock_load1 = Mock(spec=Load)
        mock_load1.load_distribution.return_value = np.ones_like(analyzer.points) * 8
        
        mock_load2 = Mock(spec=Load)
        mock_load2.load_distribution.return_value = np.ones_like(analyzer.points) * 4
        
        analyzer.case.torsional_loads = [mock_load1, mock_load2]
        
        result = analyzer.get_internal_torsion()
        expected = np.ones_like(analyzer.points) * 12
        
        np.testing.assert_array_equal(result, expected)
    
    def test_visualize(self, analyzer):
        """Test visualize method calls visualizer.render"""
        mock_visualizer = Mock()
        
        analyzer.visualize(mock_visualizer)
        
        mock_visualizer.render.assert_called_once_with(analyzer)
    
    def test_points_array_consistency(self, analyzer):
        """Test that all methods return arrays of the same shape as points"""
        methods_to_test = [
            'get_internal_axial_force',
            'get_shear_loads',
            'get_internal_shear',
            'get_internal_moments',
            'get_internal_torsion'
        ]
        
        for method_name in methods_to_test:
            method = getattr(analyzer, method_name)
            result = method()
            assert result.shape == analyzer.points.shape, f"{method_name} returned wrong shape"
    
    def test_integration_with_realistic_values(self):
        """Integration test with more realistic beam analysis scenario"""
        # Create a more realistic test case
        points = np.linspace(0, 10, 101)  # 10m beam, 101 points
        
        mock_case = Mock(spec=LoadingCase)
        mock_case.points = points
        mock_case.length = 10.0
        mock_case.axial_loads = []
        mock_case.shear_loads = []
        mock_case.point_moments = []
        mock_case.torsional_loads = []
        
        # Add a distributed load
        mock_distributed_load = Mock(spec=Load)
        # Simulate a uniform distributed load of 1000 N/m
        mock_distributed_load.load_distribution.return_value = np.ones_like(points) * 1000
        mock_case.shear_loads = [mock_distributed_load]
        
        analyzer = BeamAnalyzer(mock_case)
        
        # Test the calculation chain
        shear_loads = analyzer.get_shear_loads()
        internal_shear = analyzer.get_internal_shear()
        internal_moments = analyzer.get_internal_moments()
        
        # Verify basic properties
        assert len(shear_loads) == len(points)
        assert len(internal_shear) == len(points)
        assert len(internal_moments) == len(points)
        
        # Verify that shear loads are constant (distributed load)
        np.testing.assert_array_equal(shear_loads, np.ones_like(points) * 1000)
        
        # Verify that internal shear increases linearly
        expected_shear = np.cumsum(np.ones_like(points) * 1000)
        np.testing.assert_array_equal(internal_shear, expected_shear)


class TestBeamAnalyzerEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_points_array(self):
        """Test behavior with empty points array"""
        mock_case = Mock(spec=LoadingCase)
        mock_case.points = np.array([])
        mock_case.length = 0
        mock_case.axial_loads = []
        mock_case.shear_loads = []
        mock_case.point_moments = []
        mock_case.torsional_loads = []
        
        analyzer = BeamAnalyzer(mock_case)
        
        result = analyzer.get_internal_axial_force()
        assert len(result) == 0
    
    def test_single_point_array(self):
        """Test behavior with single point"""
        mock_case = Mock(spec=LoadingCase)
        mock_case.points = np.array([0.5])
        mock_case.length = 1.0
        mock_case.axial_loads = []
        mock_case.shear_loads = []
        mock_case.point_moments = []
        mock_case.torsional_loads = []
        
        analyzer = BeamAnalyzer(mock_case)
        
        result = analyzer.get_internal_axial_force()
        expected = np.array([0.0])
        
        np.testing.assert_array_equal(result, expected)


if __name__ == "__main__":
    pytest.main([__file__])