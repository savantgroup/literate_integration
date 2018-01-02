"""Define the package, tests, and dependencies."""

import os
from setuptools import setup, find_packages


def read_full_documentation(fname):
    """Get log documentation from README.rst."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="literate_integration",
    version="0.0.5",
    author="Terrence Reilly",
    author_email="treilly@savantgroup.com",
    description=(
        'A library for creating literate integration tests -- '
        'ensuring documentation which is less likely to be out-of-sync.'
    ),
    license="MIT",
    keywords="documentation linter development",
    url="http://git.savantgroup.com/i3/literate_integration",
    packages=find_packages(exclude=('tests', 'docs')),
    long_description=read_full_documentation('README.md'),
    entry_points={
        'console_scripts': [
            'docgen = literate_integration.driver:main',
        ],
    },
    install_requires=[],
    setup_requires=[],
    tests_require=['pytest'],
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
