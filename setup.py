""" Initialize cloned repository """
from setuptools import setup, find_packages


# find packages
PACKAGES = find_packages()

# define args
NAME = 'VSA'
MAINTAINER = 'Anmol Srivastava'
DESCRIPTION = 'Voter suppression visualization tool.'
URL = 'https://github.com/Anmol-Srivastava/voter-suppression-analysis'
LICENSE = 'MIT License'
VERSION = '1.0'

# package all args
OPTS = dict(
    name=NAME,
    maintainer=MAINTAINER,
    description=DESCRIPTION,
    url=URL,
    license=LICENSE,
    version=VERSION,
    package=PACKAGES
)


if __name__ == '__main__':
    # set up package
    setup(**OPTS)
