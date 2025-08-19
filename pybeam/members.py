from abc import ABC, abstractmethod

from pybeam.profiles import StaticProfile
from pybeam.materials import Material
from pybeam.loads import Load
from pybeam.loading_case import LoadingCase

class Member(ABC):
    loading: LoadingCase
    length: float

    @abstractmethod
    def get_weight(self) -> float:
        pass
    

class UniformMember(Member):
    def __init__(self, length: float, profile: StaticProfile, material: Material):
        self.length = length
        self.profile = profile
        self.material = material

    def get_area(self) -> float:
        return self.profile.get_area()

    def get_moment_of_inertia(self) -> float:
        return self.profile.get_moment_of_inertia()

    def get_weight(self) -> float:
        return self.length * self.profile.get_area() * self.material.density
