# ByteCraft

ByteCraft is a small educational programming-language project. It turns readable,
indentation-based scripts into stack instructions and executes them in a tiny virtual
machine. It is inspired by the architecture of simple interpreters, but uses its own
syntax, instruction set, modules, examples, and implementation.

## Features

- Variables with `set name = expression`
- Output with `show expression`
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparisons: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Conditional blocks: `when` / `otherwise`
- Repetition: `repeat while` and `repeat count`
- Built-ins: `number`, `text`, `size`, `absolute`
- Helpful line-numbered syntax errors
- Bytecode listing with `--bytecode`

## Quick start

Requires Python 3.10 or newer. No third-party packages are needed.

```bash
python -m bytecraft examples/hello.bc
python -m bytecraft examples/loops.bc --bytecode
python -m unittest discover -s tests -v
```

## Example

```text
set total = 0
repeat count 5 as item:
    set total = total + item
show "Sum:"
show total
```

## Language guide

A statement occupies one line. Blocks use four spaces (or another consistent
indentation width) after a colon.

| ByteCraft | Meaning |
|---|---|
| `set score = 10` | Assign a variable |
| `show score` | Print a value |
| `when score >= 10:` | Conditional block |
| `otherwise:` | Alternative block |
| `repeat while score < 15:` | While loop |
| `repeat count 3 as i:` | Count from 0 to 2 |
| `yes`, `no`, `nil` | Boolean and empty values |

Expressions support parentheses, unary signs, arithmetic, comparisons, and the
built-ins listed above. The language is intentionally small and designed for
learning how tokenizing, parsing, compiling, and virtual-machine execution fit
together.

## Project layout

- `bytecraft/lexer.py` — converts source text into tokens
- `bytecraft/parser.py` — builds a syntax tree
- `bytecraft/compiler.py` — emits stack bytecode
- `bytecraft/machine.py` — executes bytecode
- `bytecraft/disasm.py` — formats bytecode for inspection
- `bytecraft/cli.py` — command-line interface
- `examples/` — sample ByteCraft programs
- `tests/` — automated tests
