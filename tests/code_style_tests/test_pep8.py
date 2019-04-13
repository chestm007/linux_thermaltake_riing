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
import pep8
import os
import os.path

from base_test_object import BaseTestObject


class TestCodeFormat(BaseTestObject):
    def test_pep8(self):
        """
        verify our codebase complies with code style guidelines
        """
        style = pep8.StyleGuide(quiet=False)
        # accepted pep8 guideline deviances
        style.options.max_line_length = 122  # generally accepted limit
        style.options.ignore = ('W503', 'E402')  # operator at start of line

        errors = 0
        # check main project directory
        for root, _not_used, files in os.walk(os.path.join(os.getcwd(), 'linux_thermaltake_riing')):
            if not isinstance(files, list):
                files = [files]
            for f in files:
                if not str(f).endswith('.py'):
                    continue
                file_path = ['{}/{}'.format(root, f)]
                result = style.check_files(file_path)  # type: pep8.BaseReport
                errors = result.total_errors

        # check tests directory
        for root, _not_used, files in os.walk(os.path.join(os.getcwd(), 'tests')):
            if not isinstance(files, list):
                files = [files]
            for f in files:
                if not str(f).endswith('.py'):
                    continue
                file_path = ['{}/{}'.format(root, f)]
                result = style.check_files(file_path)  # type: pep8.BaseReport
                errors = result.total_errors

        self.assertEqual(0, errors, 'PEP8 style errors: {}'.format(errors))
