from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, 'README.rst')) as f:
    readme = f.read()

setup(
    name='bdd-tester',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    packages=find_packages(),
    scripts=[join('bin', 'bdd_tester')],
    license='MIT',
    long_description=readme,
    install_requires=[
        'lxml',
        'gherkin-official',
        'six',
    ],
)
