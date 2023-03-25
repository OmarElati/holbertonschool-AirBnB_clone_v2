#!/usr/bin/python3
import unittest
import io
from contextlib import redirect_stdout
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    def setUp(self):
        self.console = HBNBCommand()

    def test_create(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.console.onecmd('create BaseModel')
            output = buf.getvalue().strip()
        with io.StringIO() as buf, redirect_stdout(buf):
            self.console.onecmd(f'show BaseModel {output}')
            output2 = buf.getvalue().strip()
        self.assertIn(output, output2)

    def test_quit(self):
        with self.assertRaises(SystemExit):
            self.console.onecmd('quit')

    def test_EOF(self):
        with self.assertRaises(SystemExit):
            self.console.onecmd('EOF')


if __name__ == '__main__':
    unittest.main()
