# -*- coding: utf-8 -*-
#
#   mete0r.mimemsg : SOME_DESCRIPTION
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import with_statement
from contextlib import contextmanager
import os.path
import sys


def setup_dir(f):
    ''' Decorate f to run inside the directory where setup.py resides.
    '''
    setup_dir = os.path.dirname(os.path.abspath(__file__))

    def wrapped(*args, **kwargs):
        with chdir(setup_dir):
            return f(*args, **kwargs)

    return wrapped


@contextmanager
def chdir(new_dir):
    old_dir = os.path.abspath(os.curdir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


@setup_dir
def import_setuptools():
    try:
        import setuptools
        return setuptools
    except ImportError:
        pass

    import ez_setup
    ez_setup.use_setuptools()
    import setuptools
    return setuptools


@setup_dir
def readfile(path):
    if sys.version_info.major == 3:
        f = open(path, encoding='utf-8')
    else:
        f = open(path)
    with f:
        return f.read()


@setup_dir
def get_version():
    from mete0r_mimemsg import __version__
    return __version__


def alltests():
    import sys
    import unittest
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    args = sys.argv[:]
    defaults = ['--test-path', here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)


tests_require = [
    'zope.testrunner',
]


setup_info = {
    'name': 'mete0r.mimemsg',
    'version': get_version(),
    'description': 'SOME_DESCRIPTION',
    'long_description': readfile('README.rst') + readfile('CHANGES.rst'),

    'author': 'mete0r',
    'author_email': 'mete0r@sarangbang.or.kr',
    'license': 'GNU Affero General Public License v3 or later (AGPLv3+)',
    'url': 'https://github.com/mete0r/mimemsg',

    'packages': [
        'mete0r_mimemsg',
        'mete0r_mimemsg.tests',
    ],
    'package_dir': {'': '.'},
    'install_requires': [
        'docopt',
    ],
    'test_suite': '__main__.alltests',
    'tests_require': tests_require,
    'extras_require': {
        'test': tests_require,
    },
    'entry_points': {
        'console_scripts': [
            'mimemsg = mete0r_mimemsg.cli:main'
        ],
    },
    'classifiers': [
        # 'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',  # noqa
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: Implementation :: CPython',
    ],
    'keywords': [],
    # 'zip_safe': False,
}


@setup_dir
def main():
    setuptools = import_setuptools()
    setuptools.setup(**setup_info)


if __name__ == '__main__':
    main()
