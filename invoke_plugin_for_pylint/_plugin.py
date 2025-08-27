# pylint:disable=too-many-boolean-expressions
"""Pylint invoke plugin."""

from __future__ import annotations

from typing import Any

from astroid.nodes import Arguments, AssignName, FunctionDef
from pylint.checkers import BaseChecker
from pylint.checkers.variables import VariablesChecker
from pylint.lint import PyLinter


def _inject(linter: PyLinter) -> None:
    original = VariablesChecker.add_message

    def _new_add_message(*args: Any, **kwargs: Any) -> None:
        config = linter.config
        decorators = config.additional_invoke_task_decorators + [
            "invoke.tasks.task.inner",
            "invoke.tasks.task",
        ]
        node = kwargs.get("node", args[3] if len(args) > 3 else None)
        if (
            args[1] == "unused-argument"
            and isinstance(node, AssignName)
            and node.name == "context"
            and isinstance(node.parent, Arguments)
            and isinstance(node.parent.parent, FunctionDef)
            and any(
                decorator in node.parent.parent.decoratornames()
                for decorator in decorators
            )
        ):
            return
        original(*args, **kwargs)

    VariablesChecker.add_message = _new_add_message  # type:ignore[method-assign]


class InvokeChecker(BaseChecker):
    """Pylint invoke checker.

    The checker will prevent 'unused-argument' for invoke task context arguments.
    """

    name = "invoke-plugin-for-pylint"
    priority = -1
    msgs: Any = {}

    options = (
        (
            "additional-invoke-task-decorators",
            {
                "default": [],
                "type": "csv",
                "metavar": "<comma separated list>",
                "help": "",
            },
        ),
    )

    def __init__(self, linter: PyLinter):
        super().__init__(linter=linter)
        _inject(linter)


def register(linter: PyLinter) -> None:
    """Register the invoke plugin."""
    linter.register_checker(InvokeChecker(linter))
