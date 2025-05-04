"""
Setup module for the unsignedGen package.

This module uses setuptools to package the unsignedGen project, specifying its
metadata, dependencies, and entry points.
"""

from setuptools import setup, find_packages

setup(
    name='unsigned-gen',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
)
