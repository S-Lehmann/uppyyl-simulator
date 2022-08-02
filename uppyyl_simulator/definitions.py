"""This module implements global definitions for the complete package."""
import os
import pathlib

ROOT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
RES_DIR = ROOT_DIR.joinpath("res")
