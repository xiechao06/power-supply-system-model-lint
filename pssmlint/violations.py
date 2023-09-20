from pssmlint.edge import Edge


class BaseViolation:
    message: str
    rule: str

    def __init__(self, message: str, rule: str):
        self.message = message
        self.rule = rule


class EdgeViolation(BaseViolation):
    edge: Edge

    def __init__(self, message: str, rule: str, edge: Edge):
        super().__init__(message, rule)
        self.edge = edge


ViolationType = EdgeViolation
ViolationType = EdgeViolation
