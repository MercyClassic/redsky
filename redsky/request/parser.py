import json
import re
from typing import Dict

from redsky.request import Request


class HttpRequestParser:
    def __init__(self, scope: dict):
        self._scope = scope

    def parse(self) -> Request:
        headers = self.parse_headers()
        content_type = headers.get('content-type')
        body = self.parse_body(content_type)
        query_params = self.parse_query_params()
        path_params = self.parse_path_params()
        request = Request(
            http_version=self._scope['http_version'],
            method=self._scope['method'],
            path=self._scope['path'],
            query_params=query_params,
            path_params=path_params,
            headers=headers,
            body=body,
        )
        return request

    def parse_headers(self) -> Dict[str, str]:
        headers = {}
        for key, value in self._scope['headers']:
            headers[key.decode()] = value.decode()
        return headers

    def parse_body(self, content_type: str) -> Dict[str, str]:
        if content_type == 'application/json':
            return self._parse_as_json()
        elif content_type == 'application/x-www-form-urlencoded':
            return self._parse_as_form_urlencoded()

    def _parse_as_json(self) -> Dict[str, str]:
        return json.loads(self._scope['body']) if self._scope['body'] else {}

    def _parse_as_form_urlencoded(self) -> Dict[str, str]:
        body = {}
        data = self._scope['body'].decode().split('&')
        for kv in data:
            key, value = kv.split('=')
            body[key] = value
        return body

    def parse_query_params(self) -> Dict[str, str]:
        if not self._scope['query_string']:
            return {}
        query_params = {}
        queries = self._scope['query_string'].decode().split('&')
        for kv in queries:
            key, value = kv.split('=')
            query_params[key] = value
        return query_params

    def parse_path_params(self) -> Dict[str, str]:
        request_path = self._scope['path'].split('/')
        original_path = self._scope['original_path'].split('/')
        path_params = {}
        for i in range(len(original_path)):
            if re.fullmatch(r'{\w*}', original_path[i]):
                param_name = original_path[i][1:-1]
                path_params[param_name] = request_path[i]
        return path_params
