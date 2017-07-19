# BDD IATI Tester

Assess IATI data using [behaviour-driven development](https://en.wikipedia.org/wiki/Behavior-driven_development) testing.

## Wait, what?

[Here’s a blog that nicely explains the idea.](http://blog.memespring.co.uk/2014/07/16/programatically-testing-regulatory-data/)

This project is really just a wrapper around [Behave](https://pythonhosted.org/behave/) – a python version of [Cucumber](https://cucumber.io). Tests (features) are described in [the Gherkin language](http://pythonhosted.org/behave/philosophy.html#the-gherkin-language).

## Install

```shell
pip install -r requirements.txt
```

## Run

```shell
bdd_tester [IATI XML File]
```

…Or run a specific test/set of tests with e.g.:

```shell
bdd_tester --feature sample_features/iati_standard_ruleset [IATI XML File]
```

For more options, run:

```shell
bdd_tester --help
```

## API

```python
from bdd_tester import bdd_tester

bdd_tester(xml_file, features, **kwargs)
```
