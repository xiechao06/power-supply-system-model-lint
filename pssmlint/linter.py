from itertools import chain
from typing import Callable

from apssdag.connection import Connection
from apssdag.dag import AbstractPowerSupplySystemDag

from pssmlint.exceptions import LintError
from pssmlint.plugin import PssmLintPlugin
from pssmlint.rule import PssmLintRule
from pssmlint.violations import ViolationType

VisitConnectionHook = Callable[[Connection], ViolationType | None]


class PssmLinter:
    plugins: tuple[PssmLintPlugin, ...]

    _visit_connection_hooks: tuple[tuple[PssmLintRule, VisitConnectionHook], ...]

    def __init__(self, *plugins: PssmLintPlugin) -> None:
        assert len(plugins) > 0, "You should provide at least 1 plugin"
        self.plugins = plugins
        self._visit_connection_hooks = tuple(
            chain.from_iterable(plugin.visit_connection_hooks for plugin in plugins)
        )

    def lint(self, dag: AbstractPowerSupplySystemDag):
        violations: list[ViolationType] = []
        for _, hook in self._visit_connection_hooks:
            for conn in chain.from_iterable(dag.conns.values()):
                if violation := hook(conn):
                    violations.append(violation)

        if violations:
            raise LintError(violations)
