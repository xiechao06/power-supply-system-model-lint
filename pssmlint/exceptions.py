from pssmlint.violations import ConnectionViolation


class LintError(Exception):
    violations: list[ConnectionViolation]

    def __init__(self, violations: list[ConnectionViolation]):
        super().__init__()

        self.violations = violations
