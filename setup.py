from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, 'README.rst')) as f:
    readme = f.read()

test_deps = [
    'coveralls',
    'pytest',
    'pytest-cov',
]
extras = {'test': test_deps}

setup(
    name='bdd-tester',
    description='A very very basic BDD test runner',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    version='0.0.6',
    packages=find_packages(),
    scripts=[join('bin', 'bdd_tester')],
    license='MIT',
    long_description=readme,
    install_requires=[
        'gherkin-official',
        'six',
    ],
    setup_requires=['pytest-runner'],
    tests_require=test_deps,
    extras_require=extras,
)
