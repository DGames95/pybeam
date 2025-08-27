""" Beam Analyzer to compute internal forces and moments """
import numpy as np

from .loading_case import LoadingCase


class BeamAnalyzer:
    """ Analyze a loading case internal forces. Independent of beam properties """
    def __init__(self, load_case: LoadingCase):
        self.case = load_case
        self.points = load_case.points
        self.length = load_case.length

    def get_internal_axial_force(self):
        """ Get internal axial force along the beam """
        net_axial = np.zeros_like(self.points)
        for load in self.case.axial_loads:
            net_axial += load.load_distribution(self.points)
        return net_axial

    def get_shear_loads(self):
        """ Get shear loads along the beam """
        net_shear = np.zeros_like(self.points)
        for load in self.case.shear_loads:
            net_shear += load.load_distribution(self.points)
        return net_shear

    def get_moment_loads(self):
        """ Get moment loads along the beam"""
        point_moment_distribution = np.zeros_like(self.points)
        for moment in self.case.point_moments:
            point_moment_distribution += moment.load_distribution(self.points)
        return point_moment_distribution

    def get_internal_shear(self):
        """ Get internal shear along the beam """
        return np.cumsum(self.get_shear_loads())

    def get_internal_moments(self):
        """ Get internal bending moment along the beam """
        dx = self.points[1] - self.points[0]
        moment_from_shear = np.cumsum(self.get_internal_shear() * dx)
        moment_from_moments = -np.cumsum(self.get_moment_loads())

        return moment_from_shear + moment_from_moments

    def get_internal_torsion(self):
        """ Get internal torsion along the beam """
        torque_array = np.zeros_like(self.points)
        for torsion in self.case.torsional_loads:
            torque_array += torsion.load_distribution(self.points)
        return torque_array

    def visualize(self, visualizer):
        """ Visualize the loading case and results """
        visualizer.render(self)
