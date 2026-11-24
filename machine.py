import sys
from .lexer import Lexer
from .parser import Parser
from .compiler import Compiler
from .instructions import Op

class VirtualMachine:
    def __init__(self, output=None):
        self.output = output or sys.stdout
        self.stack = []
        self.variables = {}

    def execute(self, code, variables=None):
        if variables is not None:
            self.variables = variables
        self.stack = []
        ip = 0
        while ip < len(code):
            instruction = code[ip]
            ip += 1
            op, arg = instruction.op, instruction.arg
            if op == Op.CONST:
                self.stack.append(arg)
            elif op == Op.GET:
                if arg not in self.variables:
                    raise NameError(f"Variable {arg!r} has not been set")
                self.stack.append(self.variables[arg])
            elif op == Op.PUT:
                self.variables[arg] = self.stack.pop()
            elif op in (Op.ADD, Op.SUB, Op.MUL, Op.DIV, Op.MOD):
                right, left = self.stack.pop(), self.stack.pop()
                if op == Op.ADD: value = left + right
                elif op == Op.SUB: value = left - right
                elif op == Op.MUL: value = left * right
                elif op == Op.MOD: value = left % right
                else: value = left / right
                self.stack.append(value)
            elif op == Op.NEG:
                self.stack.append(-self.stack.pop())
            elif op == Op.CMP:
                right, left = self.stack.pop(), self.stack.pop()
                checks = {
                    "==": lambda: left == right, "!=": lambda: left != right,
                    "<": lambda: left < right, "<=": lambda: left <= right,
                    ">": lambda: left > right, ">=": lambda: left >= right,
                }
                self.stack.append(checks[arg]())
            elif op == Op.BRANCH_FALSE:
                if not self.stack.pop():
                    ip = arg
            elif op == Op.JUMP:
                ip = arg
            elif op == Op.INVOKE:
                name, count = arg
                args = self.stack[-count:] if count else []
                if count:
                    del self.stack[-count:]
                builtins = {"number": int, "text": str, "size": len, "absolute": abs}
                if name not in builtins:
                    raise NameError(f"Unknown ByteCraft function {name!r}")
                self.stack.append(builtins[name](*args))
            elif op == Op.DISPLAY:
                print(self.stack.pop(), file=self.output)
            elif op == Op.STOP:
                break
            else:
                raise RuntimeError(f"Unsupported instruction: {op}")
        return self.variables

def run(source, output=None, variables=None):
    tokens = Lexer(source).scan()
    tree = Parser(tokens).parse()
    code = Compiler().compile(tree)
    return VirtualMachine(output).execute(code, variables)

def compile_source(source):
    return Compiler().compile(Parser(Lexer(source).scan()).parse())
