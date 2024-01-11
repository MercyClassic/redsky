from dataclasses import dataclass
from enum import Enum
from typing import Dict, Literal


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
    query_params: Dict[str, str]
    path_params: Dict[str, str]
    headers: Dict[str, str]
    body: Dict | None
