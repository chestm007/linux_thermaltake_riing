import os
import sys
import time
import unittest

import nose
from nose.config import Config
from nose.core import TextTestRunner
from nose.result import TextTestResult


class TimeLoggingTestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_timings = []

    def startTest(self, test):
        self._started_at = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._started_at
        name = self.getDescription(test)
        self.test_timings.append((name, elapsed))
        super().addSuccess(test)


class PatchedTextTestRunner(TextTestRunner):
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1,
                 config=None, slow_test_threshold=1.0):
        self.slow_test_threshold = slow_test_threshold
        if config is None:
            config = Config()
        self.config = config
        self.result_class = TimeLoggingTestResult
        unittest.TextTestRunner.__init__(self, stream, descriptions, verbosity)

    def _makeResult(self):
        return self.result_class(self.stream,
                                 self.descriptions,
                                 self.verbosity)

    def run(self, test):
        result = super().run(test)

        self.stream.writeln(
            "\nSlow Tests (>{:.03}s):".format(
                self.slow_test_threshold))
        for name, elapsed in result.test_timings:
            if elapsed > self.slow_test_threshold:
                self.stream.writeln(
                    "({:.03}s) {}".format(
                        elapsed, name))
        return result


if __name__ == '__main__':
    # change into the base directory of this package.
    os.chdir(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])

    test_runner = PatchedTextTestRunner()

    nose.main(testRunner=test_runner)
