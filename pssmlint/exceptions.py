from pssmlint.violations import EdgeViolation


class LintError(Exception):
    violations: list[EdgeViolation]

    def __init__(self, violations: list[EdgeViolation]):
        super().__init__()

        self.violations = violations
