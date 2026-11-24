import io
import unittest
from bytecraft import run, Lexer, Parser, Compiler
from bytecraft.machine import compile_source
from bytecraft.disasm import disassemble

class ByteCraftTests(unittest.TestCase):
    def execute(self, source):
        output = io.StringIO()
        variables = run(source, output=output)
        return output.getvalue(), variables

    def test_arithmetic_and_precedence(self):
        output, env = self.execute("set answer = 8 - 3 * 2\nshow answer\n")
        self.assertEqual(output, "2\n")
        self.assertEqual(env["answer"], 2)

    def test_count_loop(self):
        output, _ = self.execute(
            "set total = 0\nrepeat count 4 as n:\n    set total = total + n\nshow total\n"
        )
        self.assertEqual(output, "6\n")

    def test_while_loop(self):
        output, _ = self.execute(
            "set n = 3\nrepeat while n > 0:\n    show n\n    set n = n - 1\n"
        )
        self.assertEqual(output, "3\n2\n1\n")

    def test_condition(self):
        output, _ = self.execute(
            'set x = 9\nwhen x < 5:\n    show "low"\notherwise:\n    show "high"\n'
        )
        self.assertEqual(output, "high\n")

    def test_literals_and_builtin(self):
        output, _ = self.execute('show size("craft")\nshow yes\nshow nil\n')
        self.assertEqual(output, "5\nTrue\nNone\n")

    def test_undefined_variable(self):
        with self.assertRaises(NameError):
            self.execute("show missing\n")

    def test_bytecode_listing(self):
        listing = disassemble(compile_source("set x = 1\nshow x\n"))
        self.assertIn("CONST", listing)
        self.assertIn("DISPLAY", listing)
        self.assertIn("STOP", listing)

if __name__ == "__main__":
    unittest.main()
