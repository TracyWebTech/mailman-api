
import os
import re
import codecs

from setuptools import setup


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts),
                       encoding='utf8').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='mailman-api',
    version=find_version('mailmanapi/__init__.py'),
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    packages=['mailmanapi'],
    package_data={'mailmanapi': ['templates/*']},
    scripts=['scripts/mailman-api'],
    url='http://pypi.python.org/pypi/mailman-api/',
    license='LICENSE.txt',
    description='REST API daemon to interact with Mailman 2',
    long_description=read('README.rst'),
    install_requires=[
        "Paste >= 1.7.5.1",
        "bottle >= 0.11.6",
    ],
)
