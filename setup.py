from distutils.core import setup
import os

from setuptools import find_packages

VERSION = os.environ.get('TRAVIS_TAG') or '0.0.1-untagged'

setup(
    name='linux_thermaltake_rgb',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/chestm007/linux_thermaltake_rgb',
    license='GPL-2.0',
    author='Max Chesterfield',
    author_email='chestm007@hotmail.com',
    description='python driver and daemon for thermaltake hardware products',
    install_requires=[
        "pyyaml",
        "gobject"
    ],
    entry_points="""
        [console_scripts]
        linux-thermaltake-rgb=main:main
    """
)