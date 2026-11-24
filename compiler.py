from .instructions import Instruction, Op
from . import parser as ast

ARITH = {"+": Op.ADD, "-": Op.SUB, "*": Op.MUL, "/": Op.DIV, "%": Op.MOD}

class Compiler:
    def __init__(self):
        self.code = []

    def emit(self, op, arg=None):
        self.code.append(Instruction(op, arg))
        return len(self.code) - 1

    def patch(self, index, target):
        self.code[index].arg = target

    def compile(self, tree):
        self.code = []
        self.visit(tree)
        self.emit(Op.STOP)
        return self.code

    def visit(self, node):
        method = getattr(self, "visit_" + type(node).__name__, None)
        if method is None:
            raise TypeError(f"Unsupported syntax node: {type(node).__name__}")
        return method(node)

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Literal(self, node): self.emit(Op.CONST, node.value)
    def visit_Variable(self, node): self.emit(Op.GET, node.name)

    def visit_Unary(self, node):
        self.visit(node.value)
        if node.op == "-":
            self.emit(Op.NEG)

    def visit_Binary(self, node):
        self.visit(node.left)
        self.visit(node.right)
        self.emit(ARITH[node.op] if node.op in ARITH else Op.CMP, None if node.op in ARITH else node.op)

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)
        self.emit(Op.INVOKE, (node.name, len(node.args)))

    def visit_SetStmt(self, node):
        self.visit(node.value)
        self.emit(Op.PUT, node.name)

    def visit_ShowStmt(self, node):
        self.visit(node.value)
        self.emit(Op.DISPLAY)

    def visit_WhenStmt(self, node):
        self.visit(node.condition)
        false_jump = self.emit(Op.BRANCH_FALSE, -1)
        for statement in node.yes_body:
            self.visit(statement)
        end_jump = self.emit(Op.JUMP, -1)
        self.patch(false_jump, len(self.code))
        for statement in node.no_body:
            self.visit(statement)
        self.patch(end_jump, len(self.code))

    def visit_WhileStmt(self, node):
        start = len(self.code)
        self.visit(node.condition)
        exit_jump = self.emit(Op.BRANCH_FALSE, -1)
        for statement in node.body:
            self.visit(statement)
        self.emit(Op.JUMP, start)
        self.patch(exit_jump, len(self.code))

    def visit_CountStmt(self, node):
        counter = f"$count_{len(self.code)}"
        limit = f"$limit_{len(self.code)}"
        self.emit(Op.CONST, 0)
        self.emit(Op.PUT, counter)
        self.visit(node.count)
        self.emit(Op.PUT, limit)
        start = len(self.code)
        self.emit(Op.GET, counter)
        self.emit(Op.GET, limit)
        self.emit(Op.CMP, "<")
        exit_jump = self.emit(Op.BRANCH_FALSE, -1)
        self.emit(Op.GET, counter)
        self.emit(Op.PUT, node.name)
        for statement in node.body:
            self.visit(statement)
        self.emit(Op.GET, counter)
        self.emit(Op.CONST, 1)
        self.emit(Op.ADD)
        self.emit(Op.PUT, counter)
        self.emit(Op.JUMP, start)
        self.patch(exit_jump, len(self.code))
