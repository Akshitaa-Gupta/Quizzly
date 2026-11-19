import sys
import os  # noqa: E402
import traceback  # noqa: E402

# Run the test suite programmatically so stdout is captured to a readable file.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Patch the test DB path first (mirrors test_quizzly.py setUpClass).
import db
import sqlite3

TEST_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "test_quizzly_model_check.db")
db.DEFAULT_DB_PATH = TEST_DB
try:
    os.remove(TEST_DB)
except FileNotFoundError:
    pass
db.init_db(TEST_DB)

import unittest
import test_quizzly

loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(test_quizzly)
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

print("=" * 60)
print("TEST_SUITE_RESULT=OK" if result.wasSuccessful() else "TEST_SUITE_RESULT=FAILURES")
print("TEST_SUITE_COUNT=" + str(result.testsRun))
print("TEST_SUITE_FAILURES=" + str(len(result.failures)))
print("TEST_SUITE_ERRORS=" + str(len(result.errors)))
sys.exit(0 if result.wasSuccessful() else 1)

