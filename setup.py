#coding: utf-8
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import debtcoin

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()




# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='debtcoin',  # Required
    version=debtcoin.__version__,  # Required
    description='debtcoin project',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown', 

    packages=find_packages(exclude=['test']),  # Required

    install_requires=['pycrypto'],
    
    use_scm_version=True,

    extras_require={
        'test': 'pytest'
        },
)
