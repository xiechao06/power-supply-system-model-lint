from itertools import chain
from typing import Callable

from apssdag.connection import Connection

from pssmlint.rule import PssmLintRule
from pssmlint.violations import ViolationType


class PssmLintPlugin:
    VisitConnectionHook = Callable[[Connection], ViolationType | None]
    name: str
    _rules: dict[str, PssmLintRule]
    visit_connection_hooks: tuple[tuple[PssmLintRule, VisitConnectionHook], ...]

    def __init__(self, name: str, *rules: PssmLintRule):
        assert len(rules) >= 1, "You should provide at least 1 rule"
        self.name = name
        self._rules = dict((rule.name, rule) for rule in rules)
        visit_connection_hooks = []
        for rule in rules:
            visit_connection_hooks.extend(
                (rule, hook) for hook in rule.visit_connection_hooks
            )
        self.visit_connection_hooks = tuple(visit_connection_hooks)
