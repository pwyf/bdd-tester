from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, 'README.rst')) as f:
    readme = f.read()

test_deps = [
    'coveralls',
]
extras = {'test': test_deps}

setup(
    name='bdd-tester',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    packages=find_packages(),
    scripts=[join('bin', 'bdd_tester')],
    test_suite='tests',
    license='MIT',
    long_description=readme,
    install_requires=[
        'lxml',
        'gherkin-official',
        'six',
    ],
    tests_require=test_deps,
    extras_require=extras,
)
