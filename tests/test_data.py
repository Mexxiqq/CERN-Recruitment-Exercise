import unittest
import logging
import os
from typing import List, Dict, Tuple
from country_picker.utils import parse_countries_json


# Set up logging to file in the same directory as this test module
log_path = os.path.join(os.path.dirname(__file__), "test_data.log")
logging.basicConfig(
    filename=log_path,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class LoggingTestResult(unittest.TextTestResult):
    """
    Custom TestResult class to log test lifecycle events:
    start, success, failure, error.
    """

    def startTest(self, test: unittest.TestCase) -> None:
        """
        Called when a test is about to start.
        Logs the test identifier.
        """
        super().startTest(test)
        logging.info(f"START   : {test.id()}")

    def addSuccess(self, test: unittest.TestCase) -> None:
        """
        Called when a test succeeds.
        Logs the test identifier with PASS status.
        """
        super().addSuccess(test)
        logging.info(f"PASS    : {test.id()}")

    def addFailure(self, test: unittest.TestCase, err) -> None:
        """
        Called when a test fails.
        Logs the test identifier and first line of failure message.
        """
        super().addFailure(test, err)
        error_msg = str(err[1]).splitlines()[0]
        logging.error(f"FAIL    : {test.id()} - {error_msg}")

    def addError(self, test: unittest.TestCase, err) -> None:
        """
        Called when a test raises an error (exception).
        Logs the test identifier and first line of error message.
        """
        super().addError(test, err)
        error_msg = str(err[1]).splitlines()[0]
        logging.error(f"ERROR   : {test.id()} - {error_msg}")


class LoggingTestRunner(unittest.TextTestRunner):
    """
    Custom TestRunner that uses LoggingTestResult for detailed logging.
    """
    resultclass = LoggingTestResult


class TestParseCountriesJson(unittest.TestCase):
    """
    Unit tests for the parse_countries_json function
    located in country_picker.utils.
    """

    def test_parse_valid_json(self) -> None:
        """
        Tests parsing valid JSON with country names and alpha2 codes.
        Checks that output is sorted and formatted as expected.
        """
        logging.info("TEST    : test_parse_valid_json")
        json_data: List[Dict] = [
            {"name": "Switzerland", "alpha2Code": "CH"},
            {"name": "United States", "alpha2Code": "US"},
            {"name": "France", "alpha2Code": "FR"},
        ]
        expected: List[Tuple[str, str]] = [
            ("France", "fr"),
            ("Switzerland", "ch"),
            ("United States", "us"),
        ]
        result = parse_countries_json(json_data)
        self.assertEqual(result, expected)

    def test_parse_missing_fields(self) -> None:
        """
        Tests that entries missing 'name' or 'alpha2Code' are skipped.
        Only entries with both fields are included in the result.
        """
        logging.info("TEST    : test_parse_missing_fields")
        json_data: List[Dict] = [
            {"name": "Switzerland"},  # missing alpha2Code
            {"alpha2Code": "US"},     # missing name
            {"name": "France", "alpha2Code": "FR"},
        ]
        expected: List[Tuple[str, str]] = [("France", "fr")]
        result = parse_countries_json(json_data)
        self.assertEqual(result, expected)

    def test_parse_empty_list(self) -> None:
        """
        Tests that parsing an empty list returns an empty list.
        """
        logging.info("TEST    : test_parse_empty_list")
        result = parse_countries_json([])
        self.assertEqual(result, [])


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str | None) -> unittest.TestSuite:
    """
    Custom load_tests function to run the tests with LoggingTestRunner
    when executing this module via `python -m unittest`.

    Args:
        loader: TestLoader instance
        tests: Initially loaded tests
        pattern: Optional pattern string

    Returns:
        An empty TestSuite to prevent double test runs.
    """
    suite = unittest.TestSuite()
    suite.addTests(tests)

    # Run tests and log results
    runner = LoggingTestRunner(verbosity=2)
    result = runner.run(suite)

    # Log a summary line after all tests finish
    logging.info(
        f"SUMMARY : Tests run: {result.testsRun}, "
        f"Failures: {len(result.failures)}, "
        f"Errors: {len(result.errors)}, "
        f"Skipped: {len(getattr(result, 'skipped', []))}"
    )

    # Return an empty suite so unittest doesn’t run the tests again
    return unittest.TestSuite()
