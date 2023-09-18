import re

import pytest
from apssdag.builder import AbstractPowerSupplySystemDagBuilder
from apssdag.connection import Connection
from apssdag.devices.power_supply import PowerSupply
from apssdag.devices.switch import Switch

from pssmlint.exceptions import LintError
from pssmlint.linter import PssmLinter
from pssmlint.plugin import PssmLintPlugin
from pssmlint.rule import PssmLintRule
from pssmlint.violations import ConnectionViolation


def test_linter():
    builder = (
        AbstractPowerSupplySystemDagBuilder()
        .add_device(PowerSupply("power_supply_1"))
        .add_device(Switch("switch_1"))
        .add_connection(
            from_="power_supply_1",
            to="switch_1",
            extras={"cool": False, "awesome": True},
        )
    )

    def be_cool(conn: Connection):
        if not conn.extras["cool"]:
            return ConnectionViolation(
                f"connection from {conn.from_.data.name} to "
                f"{conn.to.data.name} should be cool",
                "be cool",
                conn,
            )

    def be_awesome(conn: Connection):
        if not conn.extras["awesome"]:
            return ConnectionViolation(
                f"connection from {conn.from_.data.name} to "
                f"{conn.to.data.name} should be awesome",
                "be awesome",
                conn,
            )

    plugin = PssmLintPlugin(
        "my plugin",
        PssmLintRule("be cool").visit_connection(be_cool),
        PssmLintRule("be awesome").visit_connection(be_awesome),
    )

    with pytest.raises(LintError) as e:
        PssmLinter(plugin).lint(builder.build())

    assert len(e.value.violations) == 1
    violation = e.value.violations[0]
    print(violation.message)
    assert re.match(r".*should be cool$", violation.message)
