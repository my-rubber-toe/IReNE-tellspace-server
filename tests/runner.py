import unittest
from tests.test_validators import test_document
import re


# Initialize test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add your tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_document))


if __name__ == '__main__':
    # runner = unittest.TextTestRunner(verbosity=3)
    # result = runner.run(suite)
    regex = re.compile(r"^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$")
    print(bool(re.match(regex, "bobby the ripper")))

