""" Loading Case is a colleciton of all load types on a beam """

import numpy as np

from .loads import Load, MomentLoad

# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-positional-arguments
# Reason: This class is just a data container
class LoadingCase:
    """ A loading case is a collection of loads on a beam """
    def __init__(
        self,
        length: float,
        num_points: int,
        axial_loads: list[Load] | None = None,
        shear_loads: list[Load] | None = None,
        point_moments: list[MomentLoad]| None = None,
        torsional_loads: list[MomentLoad] | None = None,
        name: str = "LoadingCase"
    ):
        # avoid empty list as default
        self.axial_loads = axial_loads if axial_loads is not None else []
        self.shear_loads = shear_loads if shear_loads is not None else []
        self.point_moments = point_moments if point_moments is not None else []
        self.torsional_loads = torsional_loads if torsional_loads is not None else []
        self.length = length
        self.name = name
        self.points = np.linspace(0, length, num_points)
