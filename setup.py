#!/usr/bin/env python

"""setup.py: Controls the setup process using setuptools."""

import re

from setuptools import setup

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open("uppyyl_simulator/version.py").read(),
    re.M,
).group(1)

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(
    name="uppyyl_simulator",
    packages=["uppyyl_simulator"],
    entry_points={
        "console_scripts": [
            "uppyyl_simulator = uppyyl_simulator.__main__:main",
            "uppyyl-simulator = uppyyl_simulator.__main__:main",
        ]
    },
    version=version,
    description="Uppyyl simulator including a CLI tool.",
    long_description=long_description,
    author="Sascha Lehmann",
    author_email="s.lehmann@tuhh.de",
    project_urls={
        "Affiliation": "https://www.tuhh.de/sts",
    },
    url="",
    install_requires=[
        "numpy==1.22.4",
        "pytest==7.1.2",
        "pytest-subtests==0.8.0",
        "TatSu==5.6.1",
        "lxml==4.8.0",
        "colorama==0.4.4",
        "coverage==6.4",
    ],
)
