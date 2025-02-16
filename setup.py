

from setuptools import setup, find_namespace_packages

setup(
    name="jeu-combat",
    version="0.1",
    packages=find_namespace_packages(include=['src.*']),
    package_dir={'': '.'},
    install_requires=[],
    python_requires='>=3.6',
) 