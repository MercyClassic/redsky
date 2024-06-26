import re
from collections.abc import Callable
from typing import Any

from redsky.responses.response import BaseResponse
from redsky.routers.path_operation import PathOperation


class APIRouter:
    def __init__(self, prefix: str = ''):
        self.prefix = prefix
        self._routes = {}

    def get_routes(self) -> dict[PathOperation, Callable]:
        return self._routes

    def _register_as_method(
        self,
        controller: Callable,
        path: str,
        method: str,
    ) -> None:
        regex_path = re.sub(r'{\w*}', r'\\w*', path)
        path_operation = PathOperation(
            method=method,
            path=path,
            regex_path=regex_path,
        )
        self._routes[path_operation] = controller

    def _start_register(
        self,
        path: str,
        http_method: str,
    ) -> Callable:
        def wrapper(controller: Callable) -> Callable[[Any], BaseResponse]:
            self._register_as_method(controller, path, http_method)
            return controller
        return wrapper

    def _normalize_path(self, path: str) -> str:
        path = path.rstrip('/')
        if not path.startswith('/'):
            path = f'/{path}'
        return path

    def get(self, path: str) -> Callable:
        path = self._normalize_path(path)
        return self._start_register(path, 'GET')

    def post(self, path: str) -> Callable:
        path = self._normalize_path(path)
        return self._start_register(path, 'POST')

    def patch(self, path: str) -> Callable:
        path = self._normalize_path(path)
        return self._start_register(path, 'PATCH')

    def delete(self, path: str) -> Callable:
        path = self._normalize_path(path)
        return self._start_register(path, 'DELETE')
