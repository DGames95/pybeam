from abc import ABC, abstractmethod
import numpy as np


class Load(ABC):
    """Marker base class for all loads."""
    pass


class ForceLoad(Load):
    @abstractmethod
    def load_distribution(self, positions: np.ndarray) -> np.ndarray:
        """Returns force per unit length at each position."""
        pass


class MomentLoad(Load):
    @abstractmethod
    def load_distribution(self, positions: np.ndarray) -> np.ndarray:
        """Returns moment step at each position."""
        pass


class PointForce(ForceLoad):
    """
    Point Force 
    """
    def __init__(self, magnitude, normalized_position):

        assert 0 <= normalized_position <= 1, "Position must be normalized"

        self.magnitude = magnitude
        self.position = normalized_position

    def load_distribution(self, positions):
        data = np.zeros_like(positions)
        index = int(np.round(self.position*len(positions)))
        if self.position==1:  # deal with discretization at end
            index = -1

        data[index] = self.magnitude

        return data

