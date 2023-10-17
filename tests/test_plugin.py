# pylint: disable=missing-function-docstring

"""Tests for invoke_plugin_for_pylint._plugin."""

from __future__ import annotations

import astroid
import pytest
from pylint.checkers.variables import VariablesChecker
from pylint.lint import PyLinter
from pylint.testutils import UnittestLinter
from pylint.utils import ASTWalker
from pytest_mock import MockerFixture

from invoke_plugin_for_pylint._plugin import InvokeChecker, register

NON_TASK_UNUSED = "def foo(bar): pass"
NON_TASK_USED = "def foo(bar): bar += 2"
NON_TASK_DECORATED_UNUSED = """import contextlib
@contextlib.contextmanager
def foo(bar):
    pass
"""
NON_TASK_DECORATED_USED = """import contextlib
@contextlib.contextmanager
def foo(bar):
    bar += 2
"""
TASK_SIMPLE_UNUSED = """from invoke import task
@task
def foo(context):
    pass
"""
TASK_SIMPLE_USED = """from invoke import task
@task
def foo(context):
    context.run("foo")
"""
TASK_ARGS_UNUSED = """from invoke import task
@task("bar")
def foo(context):
    pass
"""
TASK_ARGS_USED = """from invoke import task
@task("bar")
def foo(context):
    context.run("foo")
"""
CUSTOM_TASK_UNUSED = """from invoke import task
def deco(func):
    return task(func)

@deco
def deco_task(context):
    pass
"""
CUSTOM_TASK_USED = """from invoke import task
def deco(func):
    return task(func)

@deco
def deco_task(context):
    context.run("foo")
"""


@pytest.fixture(autouse=True)
def autoreset_add_message(mocker: MockerFixture) -> None:
    mocker.patch.object(VariablesChecker, "add_message", VariablesChecker.add_message)


@pytest.mark.parametrize(
    "code,error",
    [
        (NON_TASK_UNUSED, True),
        (NON_TASK_USED, False),
        (NON_TASK_DECORATED_UNUSED, True),
        (NON_TASK_DECORATED_USED, False),
        (TASK_SIMPLE_UNUSED, True),
        (TASK_SIMPLE_USED, False),
        (TASK_ARGS_UNUSED, True),
        (TASK_ARGS_USED, False),
        (CUSTOM_TASK_UNUSED, True),
        (CUSTOM_TASK_USED, False),
    ],
)
def test(code: str, error: bool) -> None:
    linter = UnittestLinter()
    walker = ASTWalker(linter)

    checker = VariablesChecker(linter)
    checker.open()
    walker.add_checker(checker)

    node = astroid.parse(code)
    walker.walk(node)
    messages = linter.release_messages()

    if error:
        assert len(messages) == 1
        assert messages[0].msg_id == "unused-argument"
    else:
        assert not messages


@pytest.mark.parametrize(
    "code,error",
    [
        (NON_TASK_UNUSED, True),
        (NON_TASK_USED, False),
        (NON_TASK_DECORATED_UNUSED, True),
        (NON_TASK_DECORATED_USED, False),
        (TASK_SIMPLE_UNUSED, False),
        (TASK_SIMPLE_USED, False),
        (TASK_ARGS_UNUSED, False),
        (TASK_ARGS_USED, False),
        (CUSTOM_TASK_UNUSED, True),
        (CUSTOM_TASK_USED, False),
    ],
)
def test_plugin(code: str, error: bool) -> None:
    linter = UnittestLinter()
    walker = ASTWalker(linter)

    checker = VariablesChecker(linter)
    checker.open()
    walker.add_checker(checker)

    walker.add_checker(InvokeChecker(linter))

    node = astroid.parse(code)
    walker.walk(node)
    messages = linter.release_messages()

    if error:
        assert len(messages) == 1
        assert messages[0].msg_id == "unused-argument"
    else:
        assert not messages


@pytest.mark.parametrize(
    "code,error",
    [
        (NON_TASK_UNUSED, True),
        (NON_TASK_USED, False),
        (NON_TASK_DECORATED_UNUSED, True),
        (NON_TASK_DECORATED_USED, False),
        (TASK_SIMPLE_UNUSED, False),
        (TASK_SIMPLE_USED, False),
        (TASK_ARGS_UNUSED, False),
        (TASK_ARGS_USED, False),
        (CUSTOM_TASK_UNUSED, False),
        (CUSTOM_TASK_USED, False),
    ],
)
def test_plugin_with_option(code: str, error: bool) -> None:
    linter = UnittestLinter()
    walker = ASTWalker(linter)

    checker = VariablesChecker(linter)
    checker.open()
    walker.add_checker(checker)

    invoke_checker = InvokeChecker(linter)
    walker.add_checker(invoke_checker)
    invoke_checker.linter.config.additional_invoke_task_decorators = [".deco"]

    node = astroid.parse(code)
    walker.walk(node)
    messages = linter.release_messages()

    if error:
        assert len(messages) == 1
        assert messages[0].msg_id == "unused-argument"
    else:
        assert not messages


def test_register(mocker: MockerFixture) -> None:
    linter = mocker.Mock(spec=PyLinter)
    register(linter)
    linter.register_checker.assert_called_once()
