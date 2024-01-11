from abc import ABC, abstractmethod
from typing import Dict


class APIRouter(ABC):
    @abstractmethod
    def get_routes(self) -> Dict:
        pass
