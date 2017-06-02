from os.path import join
from setuptools import setup


requirements = """
behave==1.2.5
lxml==3.7.1
requests==2.14.2
six==1.10.0
"""

setup(
    name='bdd-tester',
    scripts=[join('bin', 'bdd_tester')],
    install_requires=requirements.strip().splitlines(),
)
