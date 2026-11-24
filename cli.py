import argparse
from pathlib import Path
from .machine import run, compile_source
from .disasm import disassemble

def main(argv=None):
    parser = argparse.ArgumentParser(prog="bytecraft", description="Run a ByteCraft script")
    parser.add_argument("file", type=Path, help="Path to a .bc source file")
    parser.add_argument("--bytecode", action="store_true", help="Print compiled instructions")
    args = parser.parse_args(argv)
    try:
        source = args.file.read_text(encoding="utf-8")
        if args.bytecode:
            print(disassemble(compile_source(source)))
            print("--- program output ---")
        run(source)
        return 0
    except (OSError, SyntaxError, NameError, ValueError, TypeError, ZeroDivisionError) as exc:
        parser.exit(1, f"bytecraft: {exc}\\n")

if __name__ == "__main__":
    raise SystemExit(main())
