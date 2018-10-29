from os.path import join
from setuptools import setup, find_packages


requirements = """
lxml==3.7.1
gherkin-official==4.1.3
six==1.10.0
"""

setup(
    name='bdd-tester',
    packages=find_packages(),
    scripts=[join('bin', 'bdd_tester')],
    install_requires=requirements.strip().splitlines(),
)
