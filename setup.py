import os

from setuptools import setup, find_packages


def read(filename: str):
    """
    Function to open a file, used for the README.rst

    Args:
        filename:
            str with the path of the file to open.

    Returns:
        opens the file.

    """
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="BCECovid19",
    version="0.1",
    package_dir={"": "src"},
    author="OncoImmunity",
    packages=find_packages("src", exclude=[]),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'), install_requires=['requests', 'Bio', 'numpy']
)
