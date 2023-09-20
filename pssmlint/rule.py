from typing import Callable

from pssmlint.edge import Edge
from pssmlint.violations import ViolationType


class PssmLintRule:
    VisitEdgeHook = Callable[[Edge], ViolationType | None]
    name: str
    visit_edge_hooks: list[VisitEdgeHook]

    def __init__(self, name: str):
        self.name = name
        self.visit_edge_hooks = []

    def visit_edge(self, hook: VisitEdgeHook):
        self.visit_edge_hooks.append(hook)
        return self
