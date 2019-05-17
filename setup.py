#!/usr/bin/env python
"""Setup script for the project."""

from __future__ import print_function

import codecs
import os
import re

from setuptools import Command, setup

IMPORT = 'sphinxcontrib.disqus'
INSTALL_REQUIRES = ['sphinx']
LICENSE = 'MIT'
NAME = 'sphinxcontrib-disqus'
VERSION = '2.0.19'


def readme(path='README.rst'):
    """Try to read README.rst or return empty string if failed.

    :param str path: Path to README file.

    :return: File contents.
    :rtype: str
    """
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    handle = None
    url_prefix = 'https://raw.githubusercontent.com/wdk-docs/{name}/v{version}/'.format(name=NAME, version=VERSION)
    try:
        handle = codecs.open(path, encoding='utf-8')
        return handle.read(131072).replace('.. image:: docs', '.. image:: {0}docs'.format(url_prefix))
    except IOError:
        return ''
    finally:
        getattr(handle, 'close', lambda: None)()


class CheckVersion(Command):
    """Make sure version strings and other metadata match here, in module/package, tox, and other places."""

    description = 'verify consistent version/etc strings in project'
    user_options = []

    @classmethod
    def initialize_options(cls):
        """Required by distutils."""
        pass

    @classmethod
    def finalize_options(cls):
        """Required by distutils."""
        pass

    @classmethod
    def run(cls):
        """Check variables."""
        project = __import__(IMPORT, fromlist=[''])
        for expected, var in [('@BandCap', '__author__'), (LICENSE, '__license__'), (VERSION, '__version__')]:
            if getattr(project, var) != expected:
                raise SystemExit('Mismatch: {0}'.format(var))
        # Check changelog.
        if not re.compile(r'^%s - \d{4}-\d{2}-\d{2}$' % VERSION, re.MULTILINE).search(readme()):
            raise SystemExit('Version not found in readme/changelog file.')
        # Check tox.
        if INSTALL_REQUIRES:
            section = re.compile(r'\ninstall_requires =\n(.+?)\n\w', re.DOTALL).findall(readme('tox.ini'))
            if not section:
                raise SystemExit('Missing install_requires section in tox.ini.')
            in_tox = re.findall(r'    ([^=]+)==[\w\d.-]+', section[0])
            if INSTALL_REQUIRES != in_tox:
                raise SystemExit('Missing/unordered pinned dependencies in tox.ini.')


setup(
    author='@BandCap',
    author_email='bandcap@d3f.pw',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Plugins',
        'Environment :: Win32 (MS Windows)',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],
    cmdclass=dict(check_version=CheckVersion),
    description='Sphinx extension that embeds Disqus comments in documents.',
    install_requires=INSTALL_REQUIRES,
    keywords='sphinx disqus',
    license=LICENSE,
    long_description=readme(),
    name=NAME,
    package_data={'': [os.path.join('_static', 'disqus.js')]},
    packages=['sphinxcontrib'],
    url='https://github.com/wdk-docs/' + NAME,
    version=VERSION,
    zip_safe=False,
)
