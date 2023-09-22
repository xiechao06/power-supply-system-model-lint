import re

import pytest
from apssm.devices.power_supply import PowerSupply
from apssm.devices.switch import Switch
from apssm.gen_port_id import gen_port_id
from apssm.graph import AbstractPowerSupplySystemGraph

from pssmlint.edge import Edge
from pssmlint.exceptions import LintError
from pssmlint.linter import PssmLinter
from pssmlint.plugin import PssmLintPlugin
from pssmlint.rule import PssmLintRule
from pssmlint.violations import EdgeViolation


def test_linter():
    graph = AbstractPowerSupplySystemGraph()
    graph.add_device(PowerSupply("power_supply_1"))
    graph.add_device(Switch("switch_1"))
    graph.add_edge(
        first=("power_supply_1", 0),
        second=("switch_1", 0),
        extras={"cool": False, "awesome": True},
    )

    def be_cool(conn: Edge):
        if not conn.extras["cool"]:
            first = gen_port_id(conn.first[0].name, conn.first[1])
            second = gen_port_id(conn.second[0].name, conn.second[1])

            return EdgeViolation(
                f"connection from {first} to " f"{second} should be cool",
                "be cool",
                conn,
            )

    def be_awesome(conn: Edge):
        if not conn.extras["awesome"]:
            first = gen_port_id(conn.first[0].name, conn.first[1])
            second = gen_port_id(conn.second[0].name, conn.second[1])
            return EdgeViolation(
                f"connection from {first} to " f"{second} should be awesome",
                "be awesome",
                conn,
            )

    plugin = PssmLintPlugin(
        "my plugin",
        PssmLintRule("be cool").visit_edge(be_cool),
        PssmLintRule("be awesome").visit_edge(be_awesome),
    )

    with pytest.raises(LintError) as e:
        PssmLinter(plugin).lint(graph)

    assert len(e.value.violations) == 1
    violation = e.value.violations[0]
    assert re.match(r".*should be cool$", violation.message)
