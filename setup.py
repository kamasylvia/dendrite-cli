from pathlib import Path
from setuptools import setup, find_packages

install_requires = [
    "gitpython>=3.1.29"
]

setup(
    name="dendrite-cli",
    version="0.0.1",
    author="Kamasylvia",
    author_email="contact@kamasylvia.com",
    packages=find_packages(),
    description="dendrite setup cli",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    license="BSD",
    install_requires=install_requires,
    python_requires=">=3.7",
    entry_points={"console_scripts": ["dendrite=sample:main"]},
)
