import ast
import io
import tokenize
from .tokens import Token

KEYWORDS = {"set", "show", "when", "otherwise", "repeat", "while", "count", "as",
            "yes", "no", "nil"}

class Lexer:
    def __init__(self, source: str):
        self.source = source

    def scan(self):
        result = []
        try:
            raw = tokenize.tokenize(io.BytesIO(self.source.encode("utf-8")).readline)
            for item in raw:
                t, s, line = item.type, item.string, item.start[0]
                if t in (tokenize.ENCODING, tokenize.ENDMARKER, tokenize.COMMENT):
                    continue
                if t in (tokenize.NL, tokenize.NEWLINE):
                    if not result or result[-1].kind != "NEWLINE":
                        result.append(Token("NEWLINE", "\\n", line))
                elif t == tokenize.INDENT:
                    result.append(Token("INDENT", s, line))
                elif t == tokenize.DEDENT:
                    result.append(Token("DEDENT", "", line))
                elif t == tokenize.NUMBER:
                    value = float(s) if any(c in s.lower() for c in ".e") else int(s, 0)
                    result.append(Token("NUMBER", value, line))
                elif t == tokenize.STRING:
                    result.append(Token("STRING", ast.literal_eval(s), line))
                elif t == tokenize.NAME:
                    if s in ("yes", "no", "nil"):
                        result.append(Token("LITERAL", {"yes": True, "no": False, "nil": None}[s], line))
                    elif s in KEYWORDS:
                        result.append(Token("KEYWORD", s, line))
                    else:
                        result.append(Token("NAME", s, line))
                elif t == tokenize.OP:
                    result.append(Token(s, s, line))
        except (tokenize.TokenError, IndentationError, SyntaxError) as exc:
            raise SyntaxError(f"Lexing error: {exc}") from exc
        if not result or result[-1].kind != "NEWLINE":
            result.append(Token("NEWLINE", "\\n", max(1, len(self.source.splitlines()))))
        result.append(Token("EOF", None, max(1, len(self.source.splitlines()) + 1)))
        return result
