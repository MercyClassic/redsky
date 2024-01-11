import inspect
import re
from dataclasses import dataclass
from typing import Callable, Dict

import redsky.request as request_module
from redsky.interfaces.routers import APIRouter
from redsky.request import Request
from redsky.request.parser import HttpRequestParser
from redsky.responses.response import BaseResponse
from redsky.routers.path_operation import PathOperation


@dataclass
class Controller:
    controller: Callable
    original_path: str


class RedSky:
    def __init__(self):
        self._routes: Dict[PathOperation, Callable] = {}

    def include_router(self, router: APIRouter):
        self._routes.update(router.get_routes())

    @staticmethod
    def _add_params_to_controller(
        signature: inspect.Signature,
        request: Request,
        params: dict,
    ) -> None:
        for key, value in signature.parameters.items():
            if value.annotation == request_module.Request:
                params[key] = request
                continue
            to_pass = request.path_params.get(value.name)
            if to_pass:
                params[value.name] = to_pass

    def make_request(self, scope: dict) -> Request:
        parser = HttpRequestParser(scope)
        request = parser.parse()
        return request

    async def read_body(self, receive: Callable) -> bytes:
        body = b''
        more_body = True

        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        return body

    async def controller_not_found(self, send: Callable) -> None:
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

    def get_controller(
        self,
        path: str,
    ) -> Controller:
        for path_operation, controller in self._routes.items():
            if re.fullmatch(path_operation.regex_path, path):
                return Controller(
                    controller=controller,
                    original_path=path_operation.path,
                )

    async def __call__(self, scope, receive, send) -> None:
        scope['type'] = 'http'
        scope['path'] = scope['path'].rstrip('/')

        controller = self.get_controller(scope['path'])
        if not controller:
            await self.controller_not_found(send)
            return

        scope['body'] = await self.read_body(receive)
        scope['original_path'] = controller.original_path
        request = self.make_request(scope)

        controller = controller.controller

        params = {}
        signature = inspect.signature(controller)
        self._add_params_to_controller(
            signature,
            request,
            params,
        )

        response: BaseResponse
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
