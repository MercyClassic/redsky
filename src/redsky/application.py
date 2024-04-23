import inspect
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import redsky.request as request_module
from redsky.interfaces.routers import APIRouter
from redsky.request import Request
from redsky.request.parser import HttpRequestParser

if TYPE_CHECKING:
    from redsky.routers.path_operation import PathOperation


@dataclass
class Controller:
    controller: Callable
    original_path: str


class RedSky:
    def __init__(self) -> None:
        self._routes: dict[PathOperation, Callable] = {}

    def include_router(self, router: APIRouter) -> None:
        self._routes.update(router.get_routes())

    def _add_params_to_controller(
            self,
            signature: inspect.Signature,
            request: Request,
    ) -> dict[str, Any]:
        params = {}
        for key, value in signature.parameters.items():
            if value.annotation == request_module.Request:
                params[key] = request
                continue
            to_pass = request.path_params.get(value.name)
            if to_pass:
                params[value.name] = to_pass
        return params

    def _make_request(self, scope: dict) -> Request:
        return HttpRequestParser(scope).parse()

    async def _read_body(self, receive: Callable) -> bytes:
        body = b''
        more_body = True

        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        return body

    async def _controller_not_found(self, send: Callable) -> None:
        await send(
            {
                'type': 'http.response.start',
                'status': 404,
                'headers': [
                    [b'content-type', b'application/json'],
                    [b'content-length', b'11'],
                ],
            },
        )
        await send(
            {
                'type': 'http.response.body',
                'body': b'"Not found"',
                'more_body': False,
            },
        )

    def _get_controller(
        self,
        path: str,
    ) -> Controller | None:
        for path_operation, controller in self._routes.items():
            if re.fullmatch(path_operation.regex_path, path):
                return Controller(
                    controller=controller,
                    original_path=path_operation.path,
                )

    async def __call__(self, scope, receive, send) -> None:
        scope['type'] = 'http'
        scope['path'] = scope['path'].rstrip('/')

        controller = self._get_controller(scope['path'])
        if not controller:
            await self._controller_not_found(send)
        else:
            scope['body'] = await self._read_body(receive)
            scope['original_path'] = controller.original_path
            request = self._make_request(scope)

            controller = controller.controller

            signature = inspect.signature(controller)
            params = self._add_params_to_controller(
                signature,
                request,
            )

            if inspect.iscoroutinefunction(controller):
                response = await controller(**params)
            else:
                response = controller(**params)

            await send(
                {
                    'type': 'http.response.start',
                    'status': response.status_code,
                    'headers': response.headers,
                },
            )
            await send(
                {
                    'type': 'http.response.body',
                    'body': response.body,
                    'more_body': False,
                },
            )
