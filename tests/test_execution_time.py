"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.execution_time


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: disable=protected-access,ungrouped-imports
import unittest.mock as mock
from unittest import main as launch_tests

import PyFunceble
from helpers import BaseStdout
from PyFunceble.config import load_configuration
from PyFunceble.execution_time import ExecutionTime


class TestExecutionTime(BaseStdout):
    """
    This class will test PyFunceble.execution_time.
    """

    def setUp(self):
        """
        This method will load everything needed for the tests
        """

        load_configuration(PyFunceble.CURRENT_DIRECTORY)
        BaseStdout.setUp(self)
        PyFunceble.CONFIGURATION["show_execution_time"] = True
        PyFunceble.CONFIGURATION["start"] = int(PyFunceble.strftime("%s"))
        PyFunceble.CONFIGURATION["end"] = int(PyFunceble.strftime("%s")) + 15

    @mock.patch("PyFunceble.execution_time.ExecutionTime._stoping_time")
    def test_calculate(self, _):
        """
        This method test the calculation of the execution time.
        """

        expected = PyFunceble.OrderedDict(
            [("days", "00"), ("hours", "00"), ("minutes", "00"), ("seconds", "15")]
        )
        actual = ExecutionTime("stop")._calculate()

        self.assertEqual(expected, actual)

    @mock.patch("PyFunceble.execution_time.ExecutionTime._calculate")
    def test_format_execution_time(self, calculate):
        """
        This method test if the printed format is the one we want.
        """

        calculate.return_value = PyFunceble.OrderedDict(
            [("days", "01"), ("hours", "12"), ("minutes", "25"), ("seconds", "15")]
        )

        actual = ExecutionTime("start").format_execution_time()
        expected = "01:12:25:15"

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
