from os.path import join
from setuptools import setup


requirements = """
behave==1.2.5
lxml==3.7.1
requests
"""

setup(
    name='bdd-tester',
    scripts=[join('bin', 'bdd_tester')],
    install_requires=requirements.strip().splitlines(),
)
