#!/usr/bin/env python
#
# MIT License
#
# Copyright (c) 2018, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory (subject to receipt of any
# required approvals from the U.S. Dept. of Energy).  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import

import sys
import os
import imp
import subprocess as sp

__all__ = []

#------------------------------------------------------------------------------#
# get the path to this directory
__this_path = os.path.abspath(os.path.dirname(__file__))


#------------------------------------------------------------------------------#
def __load_module(module_name, path):
    return imp.load_module(module_name, open(path), path, ('py', 'U', imp.PY_SOURCE))


#------------------------------------------------------------------------------#
def run():
    import timemory
    print('\n--> TiMemory has MPI support: {}\n'.format(timemory.has_mpi_support()))
    print('\n--> Running tests...\n')
    _fail = 0
    _call = 0
    _tot = timemory.timer('Total test time')
    _tot.start()
    for i in [ 'timemory', 'array', 'nested', 'simple' ]:
        _f = '{}_test'.format(i)
        _file = os.path.join(__this_path, '{}.py'.format(_f))
        t = timemory.timer('{}'.format(_f.upper()))
        t.start()
        print ('\n--> [ Running {} ] ...\n'.format(_f))
        try:
            _call += 1
            sp.check_call([sys.executable, _file], cwd=os.getcwd())
        except:
            _fail += 1
        t.stop()
        print('\n\n>>>>>>> {} <<<<<<<\n\n'.format(t))
    print('\n\n============== TESTS: {}/{} PASSED   =============='.format(_call-_fail, _call))
    print('============== TESTS: {}/{} FAILURES ==============\n\n'.format(_fail, _call))
    _tot.stop()
    print('\n\n>>>>>>> {} <<<<<<<\n\n'.format(_tot))
