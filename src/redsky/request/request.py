from dataclasses import dataclass
from enum import Enum
from typing import Literal


class HttpVersion(Enum):
    first = '1.1'
    second = '2'


class HttpMethod(Enum):
    get = 'GET'
    post = 'POST'
    put = 'PUT'
    patch = 'PATCH'
    delete = 'DELETE'


@dataclass
class Request:
    http_version: Literal[
        HttpVersion.first,
        HttpVersion.second,
    ]
    method: Literal[
        HttpMethod.get,
        HttpMethod.post,
        HttpMethod.put,
        HttpMethod.patch,
        HttpMethod.delete,
    ]
    path: str
    query_params: dict[str, str]
    path_params: dict[str, str]
    headers: dict[str, str]
    body: dict[str, str] | None
