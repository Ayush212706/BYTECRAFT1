from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Token:
    kind: str
    value: Any
    line: int
