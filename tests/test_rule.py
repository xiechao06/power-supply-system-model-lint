from pssmlint.rule import PssmLintRule


def test_rule():
    rule = PssmLintRule("foo_rule").visit_connection(lambda _: None)
    assert len(rule.visit_connection_hooks) == 1
