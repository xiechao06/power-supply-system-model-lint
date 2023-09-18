from typing import Callable

from apssdag.connection import Connection

from pssmlint.violations import ViolationType


class PssmLintRule:
    VisitConnectionHook = Callable[[Connection], ViolationType | None]
    name: str
    visit_connection_hooks: list[VisitConnectionHook]

    def __init__(self, name: str):
        self.name = name
        self.visit_connection_hooks = []

    def visit_connection(self, hook: VisitConnectionHook):
        self.visit_connection_hooks.append(hook)
        return self
