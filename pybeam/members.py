from abc import ABC, abstractmethod

from pybeam.profiles import StaticProfile
from pybeam.materials import Material
from pybeam.loads import PointMoment, PointForce
from pybeam.loading_case import LoadingCase
from pybeam.analyze import BeamAnalyzer
from pybeam.visualizers import MatplotlibVisualizer


class AbstractMember(ABC):
    length: float

    @abstractmethod
    def get_weight(self) -> float:
        pass


class Loadable():
    loading: LoadingCase
            
    def __init__(self, length, resolution, name="loading"):
        self.loading = LoadingCase(length=length, num_points=resolution, name=name)


    def add_axial_load(self, magnitude: float, position: float):
        """
        Add an axial point force to the member.

        Args:
            magnitude: The magnitude of the axial force.
            position: The relative position along the member (from 0 to 1).
        """
        self.loading.axial_loads.append(PointForce(magnitude, position))

    def add_shear_load(self, magnitude: float, position: float):
        """
        Add a shear point force to the member.

        Args:
            magnitude: The magnitude of the shear force.
            position: The relative position along the member (from 0 to 1).
        """
        self.loading.shear_loads.append(PointForce(magnitude, position))

    def add_moment_load(self, magnitude: float, position: float):
        """
        Add a point moment to the member.

        Args:
            magnitude: The magnitude of the moment.
            position: The relative position along the member (from 0 to 1).
        """
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

    def save_plot(self, filename: str, fileformat: str="png", save_folder=None, visualizer_cls=MatplotlibVisualizer):
        """
        Analyze and save the plot to a file.

        Args:
            filename: The prefix for the saved file name.
            fileformat: The format of the saved image, either 'png' or 'pdf'. Defaults to 'png'.
            save_folder: The folder to save the image. If None, the image will be saved to the system's temporary directory.
            visualizer_cls: The visualizer class to use. Defaults to MatplotlibVisualizer.
        """
        analyzer = self.analyze()
        vis = visualizer_cls(show=False, save=True, save_folder=save_folder, fileformat=fileformat, filename_prefix=filename)
        analyzer.visualize(vis)


class UniformMember(AbstractMember, Loadable):
    def __init__(self, length: float, profile: StaticProfile, material: Material, name="uniform-member", resolution=1000):
        super().__init__(length=length, resolution=resolution, name=name)  # Call Loadable.__init__
        self.length = length
        self.profile = profile
        self.material = material

    def get_area(self) -> float:
        return self.profile.get_area()

    def get_moment_of_inertia(self) -> float:
        return self.profile.get_moment_of_inertia()

    def get_weight(self) -> float:
        return self.length * self.profile.get_area() * self.material.density
