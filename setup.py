from distutils.core import setup

from setuptools import find_packages

with open('README.md') as f:
    readme = f.read()


DATA_FILE_LOCATION = '/usr/share/linux_thermaltake_rgb'
setup(
    name='linux_thermaltake_rgb',
    version='PROJECTVERSION',
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
        "GObject",
        "psutil",
        "pyusb",
        "matplotlib",
        "scipy",
        "numpy"
    ],
    entry_points="""
        [console_scripts]
        linux-thermaltake-rgb=linux_thermaltake_rgb.daemon.main:main
    """,
    data_files=[(DATA_FILE_LOCATION, ['linux_thermaltake_rgb/assets/linux-thermaltake-rgb.service']),
                (DATA_FILE_LOCATION, ['linux_thermaltake_rgb/assets/config.yml'])]
)
