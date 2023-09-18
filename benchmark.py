#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Benchmark linter

@Author Chao.Xie
@Email xiechao06@gmail.com
"""

import time
from typing import NamedTuple

from apssdag.builder import AbstractPowerSupplySystemDagBuilder
from apssdag.connection import Connection
from apssdag.dag import AbstractPowerSupplySystemDag
from apssdag.devices.bus import Bus
from apssdag.devices.dc_dc_converter import DcDc
from apssdag.devices.load import Load
from apssdag.devices.power_supply import PowerSupply
from apssdag.devices.switch import Switch
from tabulate import tabulate
from tqdm import tqdm

from pssmlint.exceptions import LintError
from pssmlint.linter import PssmLinter
from pssmlint.plugin import PssmLintPlugin
from pssmlint.rule import PssmLintRule
from pssmlint.violations import ConnectionViolation


def gen_dag(
    power_supply_cnt: int, loads_under_bus: int
) -> AbstractPowerSupplySystemDag:
    builder = AbstractPowerSupplySystemDagBuilder()

    for i in range(power_supply_cnt):
        power_supply_name = f"power_supply_{i}"
        switch_name = f"switch_0_{i}"
        dc_dc_name = f"dc_dc_{i}"
        bus_name = f"bus_{i}"
        builder.add_device(PowerSupply(power_supply_name))
        builder.add_device(Switch(switch_name))
        builder.add_connection(from_=power_supply_name, to=switch_name)

        builder.add_device(DcDc(dc_dc_name))
        builder.add_connection(from_=switch_name, to=dc_dc_name)

        builder.add_device(Bus(bus_name))
        builder.add_connection(from_=dc_dc_name, to=bus_name)

        for j in range(loads_under_bus):
            switch_name = f"switch_1_{i}_{j}"
            load_name = f"load_{i}_{j}"
            builder.add_device(Switch(switch_name))
            builder.add_connection(from_=bus_name, to=switch_name)
            builder.add_device(Load(load_name))
            builder.add_connection(
                from_=switch_name, to=load_name, extras={"redundancy": j}
            )

    return builder.build()


def redundancy_check(rule_name: str, i: int):
    def _redundancy_check(conn: Connection):
        if conn.extras and conn.extras.get("redundancy") == i:
            return ConnectionViolation(
                message=f"redundancy should be {i}", rule=rule_name, connection=conn
            )

    return _redundancy_check


def build_plugins() -> list[PssmLintPlugin]:
    plugins = []
    for i in range(30):
        rule_name = f"redundancy should be {i}"
        rule = PssmLintRule(rule_name).visit_connection(redundancy_check(rule_name, i))
        plugin = PssmLintPlugin(f"plugin {i}", rule)
        plugins.append(plugin)

    return plugins


class Profile(NamedTuple):
    power_supply_cnt: int
    loads_under_bus: int
    runs: int


class Benchmark(NamedTuple):
    total_in_ns: int
    avg_in_ns: int
    nodes: int
    conns: int
    runs: int


def main():
    profiles = [
        Profile(10, 50, 10000),
        Profile(100, 100, 10000),
    ]
    benchs: list[Benchmark] = []
    for profile in profiles:
        dag = gen_dag(profile.power_supply_cnt, profile.loads_under_bus)
        print()

        plugins = build_plugins()

        start = time.time()
        try:
            linter = PssmLinter(*plugins)
            for _ in tqdm(range(profile.runs)):
                linter.lint(dag)
        except LintError:
            pass
        duration = round((time.time() - start) * 1e9)
        benchs.append(
            Benchmark(
                total_in_ns=duration,
                avg_in_ns=round(duration / profile.runs),
                nodes=len(dag.nodes),
                conns=sum(len(conns_) for conns_ in dag.conns.values()),
                runs=profile.runs,
            )
        )
    t = tabulate(
        [
            [
                bench.total_in_ns,
                bench.avg_in_ns,
                bench.nodes,
                bench.conns,
                bench.runs,
                30,
            ]
            for bench in benchs
        ],
        headers=["total(ns)", "avg(ns)", "nodes", "conns", "runs", "rules"],
    )
    print(t)


if __name__ == "__main__":
    main()
