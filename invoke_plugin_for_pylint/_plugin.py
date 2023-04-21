# pylint:disable=too-many-arguments,too-many-boolean-expressions
"""Pylint invoke plugin."""

from __future__ import annotations

from typing import Any

import pylint
from astroid.nodes import Arguments, AssignName, FunctionDef, NodeNG
from pylint.checkers import BaseChecker
from pylint.checkers.variables import VariablesChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter

_PL14 = pylint.__version__ > "2.14"

if pylint.__version__ < "2.11":  # pragma: no cover
    raise RuntimeError(f"pylint 2.11+ is required but found {pylint.__version__}")


def _inject(checker: BaseChecker, linter: PyLinter) -> None:
    original = VariablesChecker.add_message

    def _new_add_message(
        self: Any,
        msgid: str,
        line: Any = None,
        node: NodeNG | None = None,
        args: Any = None,
        confidence: Any = None,
        col_offset: Any = None,
    ) -> None:
        config = linter.config if _PL14 else checker.config
        decorators = config.additional_invoke_task_decorators + [
            "invoke.tasks.task.inner",
            "invoke.tasks.task",
        ]
        if (
            msgid == "unused-argument"
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
        original(self, msgid, line, node, args, confidence, col_offset)

    VariablesChecker.add_message = _new_add_message


class InvokeChecker(BaseChecker):  # type:ignore
    """Pylint invoke checker.

    The checker will prevent 'unused-argument' for invoke task context arguments.
    """

    if not _PL14:
        __implements__ = IAstroidChecker

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

    def __init__(self, linter: PyLinter = None):
        super().__init__(linter=linter)
        _inject(self, linter)


def register(linter: PyLinter) -> None:
    """Register the invoke plugin."""
    linter.register_checker(InvokeChecker(linter))
