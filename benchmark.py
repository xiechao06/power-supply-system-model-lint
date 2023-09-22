#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Benchmark linter

@Author Chao.Xie
@Email xiechao06@gmail.com
"""

import time
from typing import NamedTuple

from apssm.devices.bus import Bus
from apssm.devices.dc_dc import DcDc
from apssm.devices.load import Load
from apssm.devices.power_supply import PowerSupply
from apssm.devices.switch import Switch
from apssm.graph import AbstractPowerSupplySystemGraph
from tabulate import tabulate

from pssmlint.edge import Edge
from pssmlint.exceptions import LintError
from pssmlint.linter import PssmLinter
from pssmlint.plugin import PssmLintPlugin
from pssmlint.rule import PssmLintRule
from pssmlint.violations import EdgeViolation


def gen_graph(
    power_supply_cnt: int, loads_under_bus: int
) -> AbstractPowerSupplySystemGraph:
    graph = AbstractPowerSupplySystemGraph()

    for i in range(power_supply_cnt):
        power_supply_name = f"power_supply_{i}"
        switch_name = f"switch_0_{i}"
        dc_dc_name = f"dc_dc_{i}"
        bus_name = f"bus_{i}"
        graph.add_device(PowerSupply(power_supply_name))
        graph.add_device(Switch(switch_name))
        graph.add_edge(first=(power_supply_name, 0), second=(switch_name, 0))

        graph.add_device(DcDc(dc_dc_name))
        graph.add_edge(first=(switch_name, 1), second=(dc_dc_name, 0))

        graph.add_device(Bus(bus_name))
        graph.add_edge(first=(dc_dc_name, 1), second=(bus_name, 0))

        for j in range(loads_under_bus):
            switch_name = f"switch_1_{i}_{j}"
            load_name = f"load_{i}_{j}"
            graph.add_device(Switch(switch_name))
            graph.add_edge(first=(bus_name, 0), second=(switch_name, 0))
            graph.add_device(Load(load_name))
            graph.add_edge(
                first=(switch_name, 1), second=(load_name, 0), extras={"redundancy": j}
            )

    return graph


def redundancy_check(rule_name: str, i: int):
    def _redundancy_check(edge: Edge):
        if edge.extras and edge.extras.get("redundancy") == i:
            return EdgeViolation(
                message=f"redundancy should be {i}", rule=rule_name, edge=edge
            )

    return _redundancy_check


def build_plugins() -> list[PssmLintPlugin]:
    plugins = []
    for i in range(30):
        rule_name = f"redundancy should be {i}"
        rule = PssmLintRule(rule_name).visit_edge(redundancy_check(rule_name, i))
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
    edges: int
    runs: int


def main():
    profiles = [
        Profile(10, 50, 10000),
        Profile(100, 100, 10000),
    ]
    benchs: list[Benchmark] = []
    for profile in profiles:
        graph = gen_graph(profile.power_supply_cnt, profile.loads_under_bus)
        print()

        plugins = build_plugins()

        start = time.time()
        try:
            linter = PssmLinter(*plugins)
            for _ in range(profile.runs):
                linter.lint(graph)
        except LintError:
            pass
        duration = round((time.time() - start) * 1e9)
        benchs.append(
            Benchmark(
                total_in_ns=duration,
                avg_in_ns=round(duration / profile.runs),
                nodes=len(graph.devices),
                edges=len(graph.edges),
                runs=profile.runs,
            )
        )
    t = tabulate(
        [
            [
                bench.total_in_ns,
                bench.avg_in_ns,
                bench.nodes,
                bench.edges,
                bench.runs,
                30,
            ]
            for bench in benchs
        ],
        headers=["total(ns)", "avg(ns)", "nodes", "edges", "runs", "rules"],
    )
    print(t)


if __name__ == "__main__":
    main()
