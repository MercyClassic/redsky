from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol

from redsky.routers.path_operation import PathOperation


class APIRouter(Protocol):
    @abstractmethod
    def get_routes(self) -> dict[PathOperation, Callable]:
        pass
