try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("CYBAW.pyx")
)