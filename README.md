[![REUSE status](https://api.reuse.software/badge/github.com/SAP/invoke-plugin-for-pylint)](https://api.reuse.software/info/github.com/SAP/invoke-plugin-for-pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPI version](https://badge.fury.io/py/invoke-plugin-for-pylint.svg)](https://badge.fury.io/py/invoke-plugin-for-pylint)
[![Coverage Status](https://coveralls.io/repos/github/SAP/invoke-plugin-for-pylint/badge.svg?branch=coveralls)](https://coveralls.io/github/SAP/invoke-plugin-for-pylint?branch=coveralls)

# Invoke Plugin for Pylint
This is a plugin for pylint which disables certain checks when using invoke.

## Installation
`pip install invoke-plugin-for-pylint`, that's it.

## Usage
Add `invoke_plugin_for_pylint` to the list of pylint plugins.

## Disabled check

* unused-argument: Each invoke task needs a context argument even if not needed.
  Therefore this plugin will find all tasks and suppress all `unused-argument` errors when related to the context argument


## Configuration

If custom decorators for invoke tasks are used which wrap `invoke.task` the
`additional-invoke-task-decorators` option by checker `invoke-plugin-for-pylint` can be used.
It's a csv list of names which indicate an invoke task.

Please note, that the names must be full qualified and reflect the name of the final function.
For example, a decorator factory called "foo" in package "bar" which returns a function called
"_inner", will result in the name "bar.foo._inner".

Example for the pyproject.toml:

```toml
[tool.pylint.invoke-plugin-for-pylint]
additional-invoke-task-decorators = [
    "my_package.foo.make_task._inner",
    "my_package.foo.make_other_task",
]
```

## Build and Publish

This project uses `setuptools` as the dependency management and build tool.
To publish a new release, follow these steps:
* Update the version in the `pyproject.toml`
* Add an entry in the changelog
* Push a new tag like `vX.X.X` to trigger the release

## Support, Feedback, Contributing

This project is open to feature requests/suggestions, bug reports etc. via [GitHub issues](https://github.com/SAP/invoke-plugin-for-pylint/issues). Contribution and feedback are encouraged and always welcome. For more information about how to contribute, the project structure, as well as additional contribution information, see our [Contribution Guidelines](CONTRIBUTING.md).

## Code of Conduct

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone. By participating in this project, you agree to abide by its [Code of Conduct](CODE_OF_CONDUCT.md) at all times.

## Licensing

Copyright 2025 SAP SE or an SAP affiliate company and invoke-plugin-for-pylint contributors. Please see our [LICENSE](LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available [via the REUSE tool](https://api.reuse.software/info/github.com/SAP/invoke-plugin-for-pylint).
