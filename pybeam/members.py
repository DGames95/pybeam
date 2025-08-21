from abc import ABC, abstractmethod

from pybeam.profiles import StaticProfile
from pybeam.materials import Material
from pybeam.loads import PointMoment, PointForce
from pybeam.loading_case import LoadingCase
from pybeam.analyze import BeamAnalyzer
from pybeam.visualizers import MatplotlibVisualizer


class Member(ABC):
    length: float

    @abstractmethod
    def get_weight(self) -> float:
        pass


class LoadableMixin():
    loading: LoadingCase

    def add_axial_load(self, magnitude: float, position: float):
        self.loading.axial_loads.append(PointForce(magnitude, position))

    def add_shear_load(self, magnitude: float, position: float):
        self.loading.shear_loads.append(PointForce(magnitude, position))

    def add_moment_load(self, magnitude: float, position: float):
        self.loading.point_moments.append(PointMoment(magnitude, position))

    def analyze(self) -> BeamAnalyzer:
        """Return a BeamAnalyzer for this member's loading case."""
        return BeamAnalyzer(self.loading)

    def plot(self, visualizer_cls=MatplotlibVisualizer):
        """
        Analyze and display the plot.

        Args:
            visualizer_cls: The visualizer class to use. Defaults to MatplotlibVisualizer.
        """
        analyzer = self.analyze()
        vis = visualizer_cls()
        analyzer.visualize(vis)


class UniformMember(Member, LoadableMixin):
    def __init__(self, length: float, profile: StaticProfile, material: Material, name="uniform-member"):
        self.length = length
        self.profile = profile
        self.material = material
        self.loading = LoadingCase(length=length, num_points=100, name=name)

    def get_area(self) -> float:
        return self.profile.get_area()

    def get_moment_of_inertia(self) -> float:
        return self.profile.get_moment_of_inertia()

    def get_weight(self) -> float:
        return self.length * self.profile.get_area() * self.material.density
