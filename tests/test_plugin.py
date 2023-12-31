from pssmlint.plugin import PssmLintPlugin
from pssmlint.rule import PssmLintRule


def test_plugin():
    rule = PssmLintRule("foo_rule").visit_edge(lambda _: None)
    plugin = PssmLintPlugin("foo_plugin", rule)

    assert len(plugin.visit_edge_hooks) == 1
