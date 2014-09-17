
from distutils.core import setup

setup(
    name='mailman-api',
    version='0.1.0',
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    packages=['mailmanapi'],
    scripts=['scripts/mailman-api.py'],
    url='http://pypi.python.org/pypi/mailman-api/',
    license='LICENSE.txt',
    description='RESTful API to access some funcionalities of Mailman 2',
    long_description=open('README.rst').read(),
    install_requires=[
        "Paste >= 1.7.5.1",
        "bottle >= 0.11.6",
    ],
)
