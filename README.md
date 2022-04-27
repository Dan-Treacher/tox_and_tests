# tox_and_tests
Repo for some simple scripts testing how to work with tox and possibly unit tests

## Scope
Tox is a tool for both running tests and managing virtual environments and development tasks automatically. It operates using a tox.ini file which comprises descriptions of user defined environments within which specific commands may be run.

## Tox.ini
Each virtual environment you want to create is refered to as a *testenv* in the tox.ini file.
The example tox.ini file below, the workflow is such that

1. Tox reads config from the tox.ini file
2. Optionally creates a python package
3. Creates a python virtual environment using the python versions specified in tox.ini
4. Installs the dependencies in the *deps = * section of the tox.ini file
5. Run the commands in the *commands = * section of the tox.ini file
6. Print to stdout how each of the commands have gone

Note that the virtual environments are cached at stages during build, so if there's a crash in the command once the dependencies have been installed, rerunning will be quite quick

### Example 1
```
[tox]
envlist   = tests
skipsdist = true

[testenv]
deps =
    tests: -r requirements.txt
    lint:  flake8
    docs:  sphinx-autobuild
commands =
    tests: pytest tests/
    lint:  flake8 src
    docs:  sphinx ...
```

## Justification
Given that the tox.ini file behaves like a config file, it's easy to make adjustments there and have a CI/CD pipeline run the whole thing from end to end. The separate virtual environments made under the hood also avoid most dependency conflicts.

## Minimum working example
```
[tox]
skipsdist = true
```