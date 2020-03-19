import unittest
from tests.test_validators import test_create_document_validator


# Initialize test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add your tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_create_document_validator))


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
