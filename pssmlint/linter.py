from typing import Callable

from apssdag.graph import AbstractPowerSupplySystemGraph

from pssmlint.edge import Edge
from pssmlint.exceptions import LintError
from pssmlint.plugin import PssmLintPlugin
from pssmlint.rule import PssmLintRule
from pssmlint.violations import ViolationType

VisitEdgeHook = Callable[[Edge], ViolationType | None]


class PssmLinter:
    plugins: tuple[PssmLintPlugin, ...]

    _visit_edge_hooks: list[tuple[PssmLintRule, VisitEdgeHook]]

    def __init__(self, *plugins: PssmLintPlugin) -> None:
        assert len(plugins) > 0, "You should provide at least 1 plugin"
        self.plugins = plugins
        self._visit_edge_hooks = []
        for plugin in plugins:
            for hook in plugin.visit_edge_hooks:
                self._visit_edge_hooks.append(hook)

    def lint(self, graph: AbstractPowerSupplySystemGraph):
        violations: list[ViolationType] = []
        for _, hook in self._visit_edge_hooks:
            for vanilla_edge in graph.edges:
                from_ = graph.nodes[vanilla_edge.from_].device
                to = graph.nodes[vanilla_edge.to].device
                edge = Edge(from_=from_, to=to, extras=vanilla_edge.extras)
                if violation := hook(edge):
                    violations.append(violation)

        if violations:
            raise LintError(violations)
