# BDD IATI Tester

Assess IATI data using [behaviour-driven development](https://en.wikipedia.org/wiki/Behavior-driven_development) testing.

## Wait, what?

[Here’s a blog that nicely explains the idea.](http://blog.memespring.co.uk/2014/07/16/programatically-testing-regulatory-data/)

~~This project is really just a wrapper around [Behave](https://pythonhosted.org/behave/) – a python version of [Cucumber](https://cucumber.io).~~ Tests (features) are described in [the Gherkin language](http://pythonhosted.org/behave/philosophy.html#the-gherkin-language).

## Install

```shell
pip install -r requirements.txt
```

## Run

```shell
bdd_tester --feature [Feature file] [IATI XML File]
```

For more options, run:

```shell
bdd_tester --help
```

## Using it programmatically

```python
from bdd_tester import bdd_tester


tester = bdd_tester(path_to_step_definitions)
feature = tester.load_feature(path_to_feature)
result = feature.tests[0](data_to_test)
```
