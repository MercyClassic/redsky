from .response import BaseResponse


class HtmlResponse(BaseResponse):
    content_type = 'text/html; charset=utf-8'

    def make_body(self, body: str | None) -> bytes:
        return (body if body else '').encode()
