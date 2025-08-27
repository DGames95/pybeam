"""Material properties for beam sizing."""

from dataclasses import dataclass

@dataclass
class Material:
    """Base class for material properties used for sizing."""
    name: str
    density: float
    modulus: float
    tensile_yield_strength: float
    shear_strength: float
    compressive_strength: float

@dataclass
class Steel(Material):
    """
    Material properties for Steel.
    
    Source: https://beamdimensions.com/materials/Steel/American_Standard_(ASTM)/ASTM_A36/
    """
    name: str = "Steel A36"
    density: float = 7850  # kg/m^3
    modulus: float = 200e9  # Pa
    tensile_yield_strength: float = 250e6  # Pa
    shear_strength: float = 250e6  # Pa
    compressive_strength: float = 500e6  # Pa
