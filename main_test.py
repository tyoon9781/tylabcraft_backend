from myapplication.database.connection import ConnectDB
from dotenv import load_dotenv
import unittest
import sys

if __name__ == "__main__":
    load_dotenv()
    ConnectDB.is_test = True

    test_loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()
    
    tests = test_loader.discover(start_dir="myapplication/test", pattern="test*.py")
    result = runner.run(tests)

    ## pre-commit
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)