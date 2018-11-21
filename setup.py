import os
import time
from distutils.core import setup

from setuptools import find_packages

with open('README.md') as f:
    readme = f.read()

VERSION = os.environ.get('TRAVIS_TAG') or '0.0.0-{}'.format(time.time())

setup(
    name='linux_thermaltake_rgb',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/chestm007/linux_thermaltake_rgb',
    license='GPL-2.0',
    author='Max Chesterfield',
    author_email='chestm007@hotmail.com',
    maintainer='Max Chesterfield',
    maintainer_email='chestm007@hotmail.com',
    description='python driver and daemon for thermaltake hardware products',
    long_description=readme,
    install_requires=[
        "pyyaml",
        "PyGObject",
        "dbus-python",
        "psutil",
        "pyusb"
    ],
    entry_points="""
        [console_scripts]
        linux-thermaltake-rgb=linux_thermaltake_rgb.daemon.main:main
    """,
    data_files=[('/etc/udev/rules.d', ['linux_thermaltake_rgb/assets/90-linux_thermaltake_rgb.rules']),
                ('/usr/lib/systemd/user', ['linux_thermaltake_rgb/assets/linux-thermaltake-rgb.service']),
                ('/etc/linux_thermaltake_rgb', ['linux_thermaltake_rgb/assets/config.yml'])]
)
