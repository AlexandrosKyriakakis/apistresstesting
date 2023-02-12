import io
import sys
import unittest

from src.run import serve


class TestServe(unittest.TestCase):
    def test_serve(self) -> None:
        captured_output = io.StringIO()
        sys.stdout = captured_output

        result = serve()

        sys.stdout = sys.__stdout__

        self.assertEqual(result, True)
        self.assertEqual(captured_output.getvalue().strip(), 'started')
