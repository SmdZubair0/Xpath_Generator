from abc import ABC, abstractmethod

class LocatorStrategy(ABC):
    @abstractmethod
    def create(self, locator: str) -> dict:
        pass