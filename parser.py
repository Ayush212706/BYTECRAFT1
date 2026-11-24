from dataclasses import dataclass, field
from .tokens import Token

@dataclass
class Node: pass
@dataclass
class Literal(Node): value: object
@dataclass
class Variable(Node): name: str
@dataclass
class Unary(Node): op: str; value: Node
@dataclass
class Binary(Node): left: Node; op: str; right: Node
@dataclass
class Call(Node): name: str; args: list
@dataclass
class SetStmt(Node): name: str; value: Node
@dataclass
class ShowStmt(Node): value: Node
@dataclass
class WhenStmt(Node):
    condition: Node
    yes_body: list
    no_body: list = field(default_factory=list)
@dataclass
class WhileStmt(Node): condition: Node; body: list
@dataclass
class CountStmt(Node): name: str; count: Node; body: list
@dataclass
class Program(Node): statements: list

class Parser:
    def __init__(self, tokens):
        self.tokens, self.pos = tokens, 0

    def current(self):
        return self.tokens[min(self.pos, len(self.tokens)-1)]

    def take(self):
        token = self.current()
        self.pos += 1
        return token

    def match(self, kind, value=None):
        if self.current().kind == kind and (value is None or self.current().value == value):
            return self.take()
        return None

    def expect(self, kind, value=None):
        token = self.match(kind, value)
        if token is None:
            wanted = value if value is not None else kind
            raise SyntaxError(f"Line {self.current().line}: expected {wanted!r}, got {self.current().value!r}")
        return token

    def parse(self):
        statements = []
        while self.current().kind != "EOF":
            if self.match("NEWLINE") or self.match("DEDENT"):
                continue
            statements.append(self.statement())
        return Program(statements)

    def block(self):
        self.expect(":")
        self.expect("NEWLINE")
        self.expect("INDENT")
        body = []
        while self.current().kind not in ("DEDENT", "EOF"):
            if self.match("NEWLINE"):
                continue
            body.append(self.statement())
        self.expect("DEDENT")
        return body

    def statement(self):
        token = self.current()
        if self.match("KEYWORD", "set"):
            name = self.expect("NAME").value
            self.expect("=")
            value = self.expression()
            self.match("NEWLINE")
            return SetStmt(name, value)
        if self.match("KEYWORD", "show"):
            value = self.expression()
            self.match("NEWLINE")
            return ShowStmt(value)
        if self.match("KEYWORD", "when"):
            condition = self.expression()
            yes_body = self.block()
            no_body = []
            if self.match("KEYWORD", "otherwise"):
                no_body = self.block()
            return WhenStmt(condition, yes_body, no_body)
        if self.match("KEYWORD", "repeat"):
            if self.match("KEYWORD", "while"):
                condition = self.expression()
                return WhileStmt(condition, self.block())
            self.expect("KEYWORD", "count")
            count = self.expression()
            self.expect("KEYWORD", "as")
            name = self.expect("NAME").value
            return CountStmt(name, count, self.block())
        raise SyntaxError(f"Line {token.line}: unexpected token {token.value!r}")

    def expression(self): return self.comparison()
    def comparison(self):
        node = self.addition()
        while self.current().kind in ("==", "!=", "<", "<=", ">", ">="):
            op = self.take().kind
            node = Binary(node, op, self.addition())
        return node
    def addition(self):
        node = self.product()
        while self.current().kind in ("+", "-"):
            op = self.take().kind
            node = Binary(node, op, self.product())
        return node
    def product(self):
        node = self.unary()
        while self.current().kind in ("*", "/", "%"):
            op = self.take().kind
            node = Binary(node, op, self.unary())
        return node
    def unary(self):
        if self.current().kind in ("+", "-"):
            return Unary(self.take().kind, self.unary())
        return self.primary()
    def primary(self):
        token = self.current()
        if token.kind in ("NUMBER", "STRING", "LITERAL"):
            self.take()
            return Literal(token.value)
        if token.kind == "NAME":
            name = self.take().value
            if self.match("("):
                args = []
                if not self.match(")"):
                    args.append(self.expression())
                    while self.match(","):
                        args.append(self.expression())
                    self.expect(")")
                return Call(name, args)
            return Variable(name)
        if self.match("("):
            node = self.expression()
            self.expect(")")
            return node
        raise SyntaxError(f"Line {token.line}: expected expression, got {token.value!r}")
