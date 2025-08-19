from dataclasses import dataclass

@dataclass
class Material:
    name: str
    density: float
    modulus: float
    tensile_strength: float
    shear_strength: float
    compressive_strength: float


class Steel(Material):
    name: str = "Steel"
    density: float = 7850  # kg/m^3
    modulus: float = 210e9  # Pa
    tensile_strength: float = 400e6  # Pa
    shear_strength: float = 250e6  # Pa
    compressive_strength: float = 500e6  # Pa