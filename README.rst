BDD IATI Tester
===============

.. image:: https://img.shields.io/travis/pwyf/bdd-tester/master.svg
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/pwyf/bdd-tester

.. image:: https://img.shields.io/coveralls/github/pwyf/bdd-tester/master.svg
    :alt: Test coverage
    :target: https://coveralls.io/github/pwyf/bdd-tester?branch=master

Assess IATI data using `behaviour-driven
development <https://en.wikipedia.org/wiki/Behavior-driven_development>`__
testing.

Wait, what?
-----------

It’s a tool to run
`Gherkin <http://pythonhosted.org/behave/philosophy.html#the-gherkin-language>`__
tests (features) against IATI data – similar to `Cucumber <https://cucumber.io>`__
(in Ruby) or `Behave <https://pythonhosted.org/behave/>`__ (in Python).
`Here’s a blog that nicely explains the idea. <http://blog.memespring.co.uk/2014/07/16/programatically-testing-regulatory-data/>`__


Install
-------

.. code:: shell

    pip install -r requirements.txt

Run
---

.. code:: shell

    bdd_tester --feature [Feature file] [IATI XML File]

For more options, run:

.. code:: shell

    bdd_tester --help

Using it programmatically
-------------------------

.. code:: python

    from bdd_tester import BDDTester


    tester = BDDTester(path_to_step_definitions)
    feature = tester.load_feature(path_to_feature)
    result = feature.tests[0](data_to_test)
