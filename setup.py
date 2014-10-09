
from setuptools import setup

setup(
    name='mailman-api',
    version='0.2.3',
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    packages=['mailmanapi'],
    package_data={'mailmanapi': ['templates/*']},
    scripts=['scripts/mailman-api'],
    url='http://pypi.python.org/pypi/mailman-api/',
    license='LICENSE.txt',
    description='REST API daemon to interact with Mailman 2',
    long_description="""mailman-api provides a daemon that will listen to HTTP requests, providing
access to a REST API that can be used to interact with a locally-installed
Mailman instance.""",
    install_requires=[
        "Paste >= 1.7.5.1",
        "bottle >= 0.11.6",
    ],
)
