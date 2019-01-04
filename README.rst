BDD Tester
==========

.. image:: https://img.shields.io/pypi/v/bdd-tester.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/bdd-tester/

.. image:: https://img.shields.io/pypi/l/bdd-tester.svg
    :alt: License
    :target: https://pypi.org/project/bdd-tester/

.. image:: https://img.shields.io/travis/pwyf/bdd-tester/master.svg
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/pwyf/bdd-tester

.. image:: https://img.shields.io/coveralls/github/pwyf/bdd-tester/master.svg
    :alt: Test coverage
    :target: https://coveralls.io/github/pwyf/bdd-tester?branch=master

Test data files using `behaviour-driven
development <https://en.wikipedia.org/wiki/Behavior-driven_development>`__
tests, in python.

Wait, what?
-----------

It’s a tool to run
`Gherkin <http://pythonhosted.org/behave/philosophy.html#the-gherkin-language>`__
tests (features) against (IATI) data – similar to `Cucumber <https://cucumber.io>`__
(in Ruby) or `Behave <https://pythonhosted.org/behave/>`__ (in Python).
`Here’s a blog that nicely explains the idea. <http://blog.memespring.co.uk/2014/07/16/programatically-testing-regulatory-data/>`__


Install
-------

.. code:: shell

    pip install bdd_tester

Run
---

.. code:: shell

    bdd_tester --feature [Feature file] --steps [Step file] [Data file]

For more options, run:

.. code:: shell

    bdd_tester --help

Using it programmatically
-------------------------

.. code:: python

    from bdd_tester import BDDTester


    tester = BDDTester(step_definitions_filepath)
    feature = tester.load_feature(feature_filepath)
    result = feature.tests[0](*args, **kwargs)
