import re
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class PathOperation:
    method: str
    path: str
    regex_path: re.compile
