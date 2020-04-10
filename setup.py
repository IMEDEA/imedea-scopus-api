
from setuptools import setup, find_packages

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='imedea_scopus_api',
    version='0.1.2',
    description='Imedea scopus access library',
    long_description=None,
    author='Jeroni Brunet Rosselló',
    author_email='jeroni@gmail.com',
    url='https://bitbucket.org/jeroni/imedea-scopus',
    license=lic,
    packages=find_packages(exclude=('testing', 'docs')),
    install_requires=[
        'PySocks',
        'msgpack-python',
    ]
)

