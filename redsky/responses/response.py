from typing import Dict, List, Tuple


class BaseResponse:
    content_type: str

    def __init__(
        self,
        status_code: int,
        body: Dict | str | None,
        headers: Dict[str, str] | None = None,
    ):
        self.status_code = status_code
        self.body = self.make_body(body)
        self.headers = self.make_headers(headers or {})

    def make_headers(self, headers: Dict[str, str]) -> List[Tuple[bytes, bytes]]:
        new_header = list()
        new_header.append((b'content-type', self.content_type.encode()))
        new_header.append((b'content-length', str(len(self.body)).encode()))
        for key, value in headers.items():
            new_header.append((key.encode(), value.encode()))
        return new_header

    def set_cookie(
        self,
        key: str,
        value: str,
        http_only: bool = None,
        max_age: int = None,
    ):
        cookie = '%s=%s' % (key, value)
        if http_only:
            cookie += '; HttpOnly'
        if max_age:
            cookie += f'; Max-Age={max_age}'
        self.headers.append((b'set-cookie', cookie.encode()))

    def delete_cookie(self, key: str):
        cookie = '%s=%s; Max-Age=0' % (key, 'deleted')
        self.headers.append((b'set-cookie', cookie.encode()))

    def make_body(self, body: Dict | str | None) -> bytes:
        raise NotImplementedError
