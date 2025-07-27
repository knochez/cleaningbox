from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="cleaningbox",
    version="1.0.3",
    author="Kevin Nochez",
    description="A lightweight, modular Python library for data cleaning workflows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/knochez/cleaningbox",
    packages=find_packages(exclude=["demo"]),
    include_package_data=True,
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "openpyxl>=3.1.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",

    entry_points={
        "console_scripts": [
            "cleaningbox=cleaningbox.__main__:main",
        ]
    }
)
