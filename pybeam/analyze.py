import numpy as np

from .loads import Load
from .loading_case import LoadingCase


class BeamAnalyzer:
    def __init__(self, load_case: LoadingCase):
        self.case = load_case
        self.points = load_case.points
        self.length = load_case.length

    def get_internal_normal_force(self):
        net_normal = np.zeros_like(self.points)
        for load in self.case.axial_loads:
            net_normal += load.load_distribution(self.points)
        return net_normal

    def get_shear_loads(self):
        net_shear = np.zeros_like(self.points)
        for load in self.case.shear_loads:
            net_shear += load.load_distribution(self.points)
        return net_shear

    def get_internal_shear(self):
        return np.cumsum(self.get_shear_loads())

    def get_internal_moments(self):
        dx = self.points[1] - self.points[0]
        moment_from_shear = np.cumsum(self.get_internal_shear() * dx)
        point_moment_distribution = np.zeros_like(self.points)
        for moment in self.case.point_moments:
            point_moment_distribution += moment.load_distribution(self.points)
        return moment_from_shear + point_moment_distribution

    def get_internal_torsion(self):
        dx = self.points[1] - self.points[0]
        torque_array = np.zeros_like(self.points)
        for torsion in self.case.torsional_loads:
            torque_array += torsion.load_distribution(self.points)
        return torque_array

    def visualize(self, visualizer):
        visualizer.render(self)