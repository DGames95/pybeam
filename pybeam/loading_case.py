import numpy as np

from .loads import Load, MomentLoad


class LoadingCase:
    def __init__(
        self,
        length: float,
        num_points: int,
        axial_loads: list[Load]=[],
        shear_loads: list[Load]=[],
        point_moments: list[MomentLoad]=[],
        torsional_loads: list[MomentLoad]=[],
        name: str = "LoadingCase"
    ):
        self.axial_loads = axial_loads
        self.shear_loads = shear_loads
        self.point_moments = point_moments
        self.torsional_loads = torsional_loads
        self.length = length
        self.name = name
        self.points = np.linspace(0, length, num_points)