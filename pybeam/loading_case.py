from typing import Iterable
import numpy as np

from .loads import Load, MomentLoad


class LoadingCase:
    def __init__(
        self,
        length: float,
        num_points: int,
        normal_loads: Iterable[Load]=[],
        shear_loads: Iterable[Load]=[],
        point_moments: Iterable[MomentLoad]=[],
        torsional_loads: Iterable[MomentLoad]=[],
        name: str = "LoadingCase"
    ):
        self.normal_loads = normal_loads
        self.shear_loads = shear_loads
        self.point_moments = point_moments
        self.torsional_loads = torsional_loads
        self.length = length
        self.name = name
        self.points = np.linspace(0, length, num_points)