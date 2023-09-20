from pssmlint.rule import PssmLintRule


def test_rule():
    rule = PssmLintRule("foo_rule").visit_edge(lambda _: None)
    assert len(rule.visit_edge_hooks) == 1
