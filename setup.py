import setuptools

from orders.__version__ import __title__, __version__, __author__, __pyversion__

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    packages = ['orders'],
    python_requires=__pyversion__
)