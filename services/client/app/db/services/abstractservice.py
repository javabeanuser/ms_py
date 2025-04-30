from abc import ABC, abstractmethod
from typing import List


class ACRUDService(ABC):

    @abstractmethod
    def get(self, *args, **kwargs) -> List[object]:
        ...

    @abstractmethod
    def create(self, *args, **kwargs):
        ...

    @abstractmethod
    def update(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...
