from typing import Callable

from pssmlint.edge import Edge
from pssmlint.rule import PssmLintRule
from pssmlint.violations import ViolationType


class PssmLintPlugin:
    VisitEdgeHook = Callable[[Edge], ViolationType | None]
    name: str
    _rules: dict[str, PssmLintRule]
    visit_edge_hooks: tuple[tuple[PssmLintRule, VisitEdgeHook], ...]

    def __init__(self, name: str, *rules: PssmLintRule):
        assert len(rules) >= 1, "You should provide at least 1 rule"
        self.name = name
        self._rules = dict((rule.name, rule) for rule in rules)
        visit_edge_hooks = []
        for rule in rules:
            visit_edge_hooks.extend((rule, hook) for hook in rule.visit_edge_hooks)
        self.visit_edge_hooks = tuple(visit_edge_hooks)
