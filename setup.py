""" Setup script for PythonEDI

"""
import re
from setuptools import setup, find_packages

setup(
    name="PythonEDI",
    description="An X12 EDI generator/parser",
    long_description="""PythonEDI uses JSON format definitions to make it easy
    to generate or read X12 EDI messages from/to Python dicts/lists.""",
    url="https://github.com/glitchassassin/python-edi",
    author="Jon Winsley",
    author_email="jon.winsley@gmail.com",
    license="MIT",
    version="0.1.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business",
        "Topic :: Text Processing"
    ],
    keywords="x12 edi 810",
    packages=find_packages(exclude=['test']),
    # package_data={"pythonedi.formats": ["810.json", "850.json", "ST.json"]},
    package_data={"pythonedi": ["formats/*.json"]},
    install_requires=['colorama'],
    include_package_data=True,
)
