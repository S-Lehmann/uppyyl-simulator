#!/usr/bin/env python

"""setup.py: Controls the setup process using setuptools."""

import re

from setuptools import setup

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('uppyyl_simulator/uppyyl_simulator.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(
    name="uppyyl_simulator",
    packages=["uppyyl_simulator"],
    entry_points={
        "console_scripts": [
            'uppyyl_simulator = uppyyl_simulator.uppyyl_simulator:main',
            'uppyyl-simulator = uppyyl_simulator.uppyyl_simulator:main',
        ]
    },
    version=version,
    description="Uppyyl simulator including a CLI tool.",
    long_description=long_description,
    author="Sascha Lehmann",
    author_email="s.lehmann@tuhh.de",
    project_urls={
        'Affiliation': 'https://www.tuhh.de/sts',
    },
    url="",
    install_requires=[
        'numpy==1.18.1',
        'pytest==5.3.5',
        'pytest-subtests==0.3.0',
        'TatSu==5.5.0',
        'lxml~=4.5.0',
        'colorama~=0.4.3',
        'coverage==5.2.1',
    ],
)
