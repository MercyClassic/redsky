

class BaseResponse:
    content_type: str

    # ignore
    def __init__(
            self,
            *,
            status_code: int,
            body: dict | str | None,
            headers: dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.body = self.make_body(body)
        self.headers = self.make_headers(headers or {})

    def make_headers(
            self,
            headers: dict[str, str],
    ) -> list[tuple[bytes, bytes]]:
        new_header = [
            (b'content-type', self.content_type.encode()),
            (b'content-length', str(len(self.body)).encode()),
        ]
        for key, value in headers.items():
            new_header.append((key.encode(), value.encode()))
        return new_header

    def set_cookie(
        self,
        key: str,
        value: str,
        http_only: bool = False,
        max_age: int | None = None,
    ):
        cookie = f'{key}={value}'
        if http_only:
            cookie += '; HttpOnly'
        if max_age:
            cookie += f'; Max-Age={max_age}'
        self.headers.append((b'set-cookie', cookie.encode()))

    def delete_cookie(self, key: str) -> None:
        cookie = f'{key}=deleted; Max-Age=0'
        self.headers.append((b'set-cookie', cookie.encode()))

    def make_body(self, body: dict | str | None) -> bytes:
        raise NotImplementedError
