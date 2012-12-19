#!/usr/bin/env python

import sys
import os
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


def get_version():
    INIT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                           'gyagp', '__init__.py'))
    f = open(INIT, 'r')
    try:
        for line in f:
            if line.startswith('__version__'):
                ret = eval(line.strip().split(' = ')[1])
                assert ret.count('.') == 2, ret
                for num in ret.split('.'):
                    assert num.isdigit(), ret
                return ret
        else:
            raise ValueError("couldn't find version string")
    finally:
        f.close()

def get_description():
    README = os.path.abspath(os.path.join(os.path.dirname(__file__), 'README'))
    f = open(README, 'r')
    try:
        return f.read()
    finally:
        f.close()

VERSION = get_version()

def main():
    setup_args = dict(
        name='gyagp',
        version=VERSION,
        download_url="http://www.gyagp.com/gyagp-%s.tar.gz" % VERSION,
        description='A small but full featured python project',
        long_description=get_description(),
        keywords=['gyagp'],
        author='Yang Gu',
        author_email='gyagp0@gmail.com',
        url='http://www.gyagp.com',
        platforms='Platform Independent',
        license='License :: OSI Approved :: BSD License',
        packages=['gyagp'],
        classifiers=[
			'Development Status :: 5 - Production/Stable',
			'Environment :: Console',
			'Natural Language :: English',
			'Operating System :: OS Independent',
			'Programming Language :: Python :: 2',
			'Topic :: Utilities',
			'Topic :: Software Development :: Libraries',
			'Topic :: Software Development :: Libraries :: Python Modules',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: BSD License',
        ],
		install_requires=[
			'pywin32',
		],  
        )

    setup(**setup_args)

if __name__ == '__main__':
    main()