# tox_and_tests
Repo for some simple scripts testing how to work with tox and possibly unit tests. The below notes are taken from *https://www.seanh.cc/2018/09/01/tox-tutorial/*.

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

## Example 1
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
Given that the tox.ini file behaves like a config file, it's easy to make adjustments there and have a CI/CD pipeline run the whole thing from end to end. The separate virtual environments made under the hood also avoid most dependency conflicts. Tox separates virtual environments by prepending the virtualenv's `bin` directory onto the subshell process path.

## Minimum working example
```
[tox]
skipsdist = true
```
With the above as your tox.ini, running *(base) > tox* from the anaconda prompt (or cmd if you have the tox installation added to windows path), then tox should make a virtual environment at *.tox/python* and run. The version of python used will be the machine default unless specified otherwise. With nothing else in the directory at runtime, the virtual environment will be built and do nothing. The successful report therefore signifies that the environment was built successfully.

The *skipsdist = true* line tells tox to **not** build an source distribution of the project (This distribution is what's required to package a project and upload it to pypi for example).

## Example 2 - Multiple commands
```
[tox] # Global settings block
skipsdist = true

[testenv]  # Block to define the testenvs
commands =
	python --version
	python -c "print('This should print these words')"
```
This is the same as the MWE, except there's now a few commands to be run in the newly created cirtual environment. This command prints the python version as output followed by a string.

## Example 3 - Command line arguments
If you have a library that runs test (for example *pytest*), you may want to be able to pass arguments to that library from the command line when actually running the *tox* command. This can be done as follows:
```
[tox]
skipsdist = true

[testenv]
deps = pytest
commands =
	python --version
	pytest --version
	pytest {posargs:tests/}
```
In the last line of the commands block, the command run in the virtualenv is *pytest <command line argument>*. The cmd line args are parsed in the form *{posargs:<default value>}*.
In this example, the default argument for that command is *tests/* making the final command *pytest tests/* which tells pytest to run all the tests in the *tests/* directory.

Additional dependencies can be included by directly calling the requirments.txt file:
```
...
deps =
	pytest
	-r requirements.txt
```
This will recursively install everything in that file too. Note however that by default, tox doesn't pick up changes to the requirements.txt file, so if you change them, you need to run *tox -r* for *rebuild* to build the virtualenv afresh instead of using a cached version.

## Example 4 - envlist
Another key used in the tox.ini file is *envlist* which specifies multiple different virtualenvs to create, beyond the single default one used above
```
[tox]
skipsdist = true
envlist = py36, py37, py38

[testenv]
commands = python --version
```
The above will run the commands once in each of the environments specified in the envlist. On my machine, the first two fail as I don't have those interpreters installed. This *envlist* can be overridden by using the *-e* command line flag in the tox command. For instance `tox -e py27` will make a Python 2.7 environment (if possible) despite it not being in the *envlist* list.

## Example 5 - Environment variables
To see all the environment variables in the virtualenv, use *commands = env*. This will show you the working environments, name etc for the process. Additional environment variables can be passed in with the *passenv* keyword:
```
...
[testenv]
passenv =
	DATABASE_URL
	GEMFURY_URL
	...
```
This will allow you to pass in these variables. Alternatively, to set them in the file, use *setenv*:
```
...
[testenv]
setenv =
	DATABASE_URL = postgresql://postgres@localhost/postgress
	GEMFURY_URL = ...
```
This doesn't seem to work very well however. Must be missing something.

## Example 6 - Conditional statments
Certain commands can be made to be conditional on other commands by using ':' to separate them. For example,
```
...
[testenv]
deps = tests:pytest
```
represents an instruction to tox to install *pytest* only in the *tests* environment.
This leads on to defining new testenvs using the conditional structure as shown in example 7


## Example 7 - Defining other environments
Using the *[testenv:NAME]* structure, we can define multiple different virtualenvs within which different dependencies, commands etc can be installed / invoked. For example:
```
[tox]  # Global config
skipsdist = true
envlist = py38

[testenv:tests]  # invoke with > tox -e tests
description = Runs the tests in python 3.6
deps = -r requirements_tests.txt  # 2.11.0
commands =
	python -c "print('Running tests testenv')"
	python -c "import requests as re; print(re.__version__)"


[testenv:somethingelse]  # invoke with > tox -e somethingelse
description = Runs something else in python 3.8
deps = -r requirements_other.txt  # 2.18.2
commands =
	python -c "print('Running something else')"
	python -c "import requests as re; print(re.__version__)"
```
Now, the following commands will be possible:
- `tox` which will run both environments and commands
- `tox -e tests` which will run only the *[testenv:tests]* environment and commands, printing 2.11.0 as the version of requests installed from requirements_tests.txt
- `tox -e somethingelse` which will run only the last environment and print the other version of the requests library as seen in the requirements_other.txt file.
- `tox -av` will print all the possible environments along with their description fields. Very handy.

A separate `[testenv]` block can be defined which contains settings that will be applied to any subsequent environments that have *testenv* as the left part of the : conditional