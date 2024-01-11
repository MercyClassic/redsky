import json
from typing import Dict

from .response import BaseResponse


class JsonResponse(BaseResponse):
    content_type = 'application/json'

    def make_body(self, body: Dict | str | None) -> bytes:
        return (json.dumps(body) if body else b'').encode()
