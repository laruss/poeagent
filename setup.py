from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name="poeagent",
    version="0.1.1",
    description="Python wrapper for Path of Exile API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Konstantin Chistiakov",
    packages=find_packages(exclude=["tests", "tests.*, test.*"]),
    install_requires=[
        "requests~=2.31.0",
        "Js2Py~=0.74",
        "beautifulsoup4~=4.12.2",
        "cloudscraper~=1.2.71",
        "websocket-client~=1.6.4",
        "appdirs~=1.4.4",
        "pydantic~=2.5.2"
    ]
)
