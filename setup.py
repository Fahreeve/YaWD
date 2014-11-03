import os
import functools
from setuptools import setup, find_packages

_IN_PACKAGE_DIR = functools.partial(os.path.join, "YaWD")

with open(_IN_PACKAGE_DIR("__version__.py")) as version_file:
    exec(version_file.read())

properties = dict(
    name="YaWD",
    classifiers = [
        "Development Status :: Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.4",
        ],
    description="A YandexWebDAV client, implemented using Requests and easywebdav",
    license="ISC",
    author="Fahreev Eldar",
    author_email="fahreeve@yandex.ru",
    url="https://github.com/fahreeve/YaWD",
    version=__version__,  # noqa
    packages=find_packages(exclude=["tests"]),
    data_files = [],
    install_requires=[
        "requests",
        "easywebdav",
        ],
    entry_points=dict(
        console_scripts=[],
        ),
    )

setup(**properties)