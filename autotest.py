#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   This file is part of autotest-pi.
#                                                                                                        
#   autotest-pi is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   autotest-pi is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with autotest-pi.  If not, see <http://www.gnu.org/licenses/>.


"""Autotest Framework

"""

__version__ = "$Revision: 1.2 $"
# $Source: /home/public/projekte/autotest-pi/autotest.py,v $

import argparse
import logging
import os.path


def parse_arguments():
    """Handle command line arguments"""

    parser = argparse.ArgumentParser(description='Autotest Framework - \
        Linogate Internet Technologies')
    parser.add_argument("test",
                        nargs='*',
                        help="list of tests")
    parser.add_argument("-d",
                        "--debug", 
                        action="store_true",
                        help="debug mode")
    parser.add_argument("--runlevel", 
                        type=int,
                        default=3,
                        help="run tests with given runlevel (1-9, default 3)")
    parser.add_argument("-v",
                        "--verbose",
                        action="count",
                        default=0,
                        help="be verbose (can be used multiple times)")
    args = parser.parse_args()
    return args
 

def setup_logging(args):
    logfilename='log/autotest.log'
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', 
                        datefmt='%d.%m.%Y %H:%M:%S',
                        filename=logfilename,level=logging.DEBUG)

def get_testlist(testparameter):
    """Verify autotests from commandline parameter.

    Arguments:
    testparameter -- cl parameters which 'should' be tests.

    Returns:
    list of tests to be performed.

    - Remove appended '/test.sh'.
    - Remove invalid directories.
    - expand directories to list of directories which contain an
      test.sh script.
    """
    autotests = []

    for test in testparameter:
        """Es gibt mehrere Möglichkeite wie die Tests als Parameter
        daherkommen:
          1.) kompletter Pfad: 'tests/firewall/incoming/test.sh'
          2.) nur Verzeichnis: 'tests/firewall/incoming'
          3.) zu expandierender Ordner: 'tests'

        Aus diesen unterschiedlichen Formen soll nun die Liste 
        autotests[] aufgebaut werden. In dieser soll der Syntax
        immer identisch sein: 'tests/pfad/zum/test'. Also
          - ohne führendes './'
          - ohne angehängtes '/test.sh'
        """
        # remove appended '/test.sh'
        if "/test.sh" in test:
            test = os.path.dirname(test)
            logging.debug("removed scriptname from parameter " + test)

        # if 'parameter/test.sh' exists, add test to autotest[]
        if os.path.isdir(test) and os.path.isfile(test + "/test.sh"):
            logging.debug("test " + test + " [OK]")
            autotests.append(test)
        elif os.path.isdir(test):
            """Das hier expandiert 'dummy/' zu 'dummy/true/test.sh', 
            dummy/false/test.sh'. Leider muss hier das test.sh 
            noch rausgeschmissen werden!
            """
            for root, dirs, files in os.walk("./"):
                for file in files:
                    if file.endswith(".sh"):
                        print("DD root:", root)
                        print("DD dirs:", dirs)
                        print("DD file:", file)
                        #autotests.append(os.path.join(root, file))
                        autotests.append(root)
        else:
            logging.info("test " + test + " not found")
    return autotests


if __name__ == '__main__':
    args = parse_arguments()
    setup_logging(args)

    if args.debug:
        print("debug mode enabled")

    # validate test-arguments
    autotests = get_testlist(args.test)
    print("Autotests:", autotests)


