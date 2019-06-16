from abc import ABC, abstractmethod

class TuxLevelGenerator(ABC):
    @abstractmethod
    def getGeneratedLevel(self):
        raise NotImplemented

    @abstractmethod
    def getGeneratorName(self):
        raise NotImplemented
