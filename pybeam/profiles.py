"""Defines various cross-section profiles for beam members."""

from abc import ABC, abstractmethod

class StaticProfile(ABC):
    """
    non varying cross-section profile
    """

    @abstractmethod
    def get_area(self) -> float:
        """Return the cross-sectional area of the profile."""

    @abstractmethod
    def get_area_moment_of_inertia(self) -> float:
        """
        Return the area moment of inertia of the profile 
        about neutral axis in shear direction.
        """


class IBeamProfile(StaticProfile):
    """I-Beam cross-section profile."""
    def __init__(self, width: float, height: float, flange_thickness: float, web_thickness: float):
        self.width = width
        self.height = height
        self.flange_thickness = flange_thickness
        self.web_thickness = web_thickness

    def get_area(self) -> float:
        # Implement the area calculation for I-Beam
        flange_area = 2 * self.flange_thickness * self.width
        web_area = self.web_thickness * (self.height - 2 * self.flange_thickness)
        return flange_area + web_area

    def get_area_moment_of_inertia(self) -> float:
        # Moment of inertia for each flange about its own centroidal axis
        flange_inertia_centroid = (self.width * self.flange_thickness**3) / 12
        # Distance from the centroid of the flange to the centroid of the I-beam
        d = (self.height / 2) - (self.flange_thickness / 2)
        # Use parallel axis theorem for both flanges
        flange_inertia = 2 * (flange_inertia_centroid + self.width * self.flange_thickness * d**2)

        web_inertia = (self.web_thickness * (self.height - 2 * self.flange_thickness)**3) / 12


        return flange_inertia + web_inertia
