#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will manage the status interface.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by
generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

In its daily usage, PyFunceble is mostly used to clean `hosts` files or blocklist.
Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains
or IPs but in the same time, it creates by default a database of the `INACTIVE`
domains or IPs so we can retest them overtime automatically at the next execution.

PyFunceble is running actively and daily with the help of Travis CI under 60+
repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, blocklists or even AdBlock
filter lists.

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
import PyFunceble
from PyFunceble.generate import Generate
from PyFunceble.lookup import Lookup


class Status(object):  # pragma: no cover  # pylint: disable=too-few-public-methods
    """
    Return the domain status in case we don't use WHOIS or in case that WHOIS
    record is not readable.

    Argument:
        - matched_result: str
            The previously catched status.
    """

    def __init__(self, matched_status):
        self.matched_status = matched_status

    def handle(self):
        """
        Handle the lack of WHOIS. :)

        Returns: str
            The status of the domains after generating the files.
        """

        source = "NSLOOKUP"

        if self.matched_status.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            if Lookup().nslookup():
                Generate(PyFunceble.STATUS["official"]["up"], source).status_file()
                return PyFunceble.STATUS["official"]["up"]

            Generate(PyFunceble.STATUS["official"]["down"], source).status_file()
            return PyFunceble.STATUS["official"]["down"]

        Generate(PyFunceble.STATUS["official"]["invalid"], "IANA").status_file()
        return PyFunceble.STATUS["official"]["invalid"]


class URLStatus(object):  # pragma: no cover  # pylint: disable=too-few-public-methods
    """
    Generate everything around the catched status.

    Argument:
        - catched_status: str
            The catched status.
    """

    def __init__(self, catched_status):
        self.catched = catched_status

    def handle(self):
        """
        Handle the backend of the given status.
        """

        source = "URL"

        if self.catched.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            Generate(self.catched, source).status_file()
        else:
            Generate(self.catched, "IANA").status_file()

        return self.catched
