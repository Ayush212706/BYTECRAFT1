from dataclasses import dataclass
from enum import Enum, auto

class Op(Enum):
    CONST = auto()
    GET = auto()
    PUT = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    NEG = auto()
    CMP = auto()
    BRANCH_FALSE = auto()
    JUMP = auto()
    INVOKE = auto()
    DISPLAY = auto()
    STOP = auto()

@dataclass
class Instruction:
    op: Op
    arg: object = None
    line: int = 1
