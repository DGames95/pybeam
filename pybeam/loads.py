from abc import ABC, abstractmethod
import numpy as np


class Load(ABC):
    @abstractmethod
    def load_distribution(self, positions: np.ndarray) -> np.ndarray:
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

class UniformDistributedLoad(Load):
    def __init__(self, w, start, end):
        assert start < end
        assert 0 <= start <= 1, "Position must be normalized"
        assert 0 <= end <= 1, "Position must be normalized"

        self.w = w
        self.start = start
        self.end = end

    def load_distribution(self, inputs):
        data = np.zeros_like(inputs)
        dx = inputs[1] - inputs[0]

        x1 = int(np.round(self.start*len(inputs)))
        x2 = int(np.round(self.end*len(inputs)))

        data[x1:x2] = self.w*dx

        return data
    
    def get_total_force(self, length):
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