# BDD IATI Tester

Assess IATI data using [behaviour-driven development](https://en.wikipedia.org/wiki/Behavior-driven_development) testing.

This project is really just a wrapper around [Behave](https://pythonhosted.org/behave/) – a python version of [Cucumber](https://cucumber.io). Tests (features) are described in [the Gherkin language](http://pythonhosted.org/behave/philosophy.html#the-gherkin-language).

# Install

```shell
pip install -r requirements.txt
```

# Run

```shell
bdd_tester [IATI XML File]
```

…or just run a single feature file e.g.

```shell
bdd_tester [IATI XML File] features/pwyf_2017/aid_type.feature
```

There’s also a bunch of extra settings provided by `behave` here. See:

```shell
bdd_tester --help
```
