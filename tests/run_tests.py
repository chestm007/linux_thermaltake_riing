"""
linux_thermaltake_rgb
Software to control your thermaltake hardware
Copyright (C) 2018  Max Chesterfield (chestm007@hotmail.com)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
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
