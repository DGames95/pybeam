"""Define loading types to be added to loading cases."""
from abc import ABC, abstractmethod
import numpy as np


class Load(ABC):
    """Abstract base class for loads."""
    @abstractmethod
    def load_distribution(self, positions: np.ndarray) -> np.ndarray:
        """Returns load at each position."""


class ForceLoad(Load):
    """ Marker class for loads in newtons"""
    @abstractmethod
    def load_distribution(self, positions: np.ndarray) -> np.ndarray:
        """Returns force per unit length at each position."""


class MomentLoad(Load):
    """ Marker class for loads in newton-meters"""
    @abstractmethod
    def load_distribution(self, positions: np.ndarray) -> np.ndarray:
        """Returns moment step at each position."""


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

class UniformDistributedLoad(Load):
    """ Uniform Distributed Load """
    def __init__(self, w, start, end):
        assert start < end
        assert 0 <= start <= 1, "Position must be normalized"
        assert 0 <= end <= 1, "Position must be normalized"

        self.w = w
        self.start = start
        self.end = end

    def load_distribution(self, positions):
        """ Get load at each position """
        data = np.zeros_like(positions)
        dx = positions[1] - positions[0]

        x1 = int(np.round(self.start*len(positions)))
        x2 = int(np.round(self.end*len(positions)))

        data[x1:x2] = self.w*dx

        return data

    def get_total_force(self, length):
        """ Get total force of the distributed load """
        return self.w*(self.end-self.start)*length


class PointMoment(MomentLoad):
    """
    Point Moment
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
