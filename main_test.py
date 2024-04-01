import unittest
import sys

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()

    tests = test_loader.discover(start_dir="myapplication/test", pattern="test*.py")
    result = runner.run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)