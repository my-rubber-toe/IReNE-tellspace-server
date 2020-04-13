import unittest
from tests.test_validators import test_document
import re
import pdfkit


# Initialize test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add your tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_document))


if __name__ == '__main__':
    pdfkit.from_file('./test.html', 'out.pdf')


