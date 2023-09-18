from apssdag.connection import Connection


class BaseViolation:
    message: str
    rule: str

    def __init__(self, message: str, rule: str):
        self.message = message
        self.rule = rule


class ConnectionViolation(BaseViolation):
    connection: Connection

    def __init__(self, message: str, rule: str, connection: Connection):
        super().__init__(message, rule)
        self.connection = connection


ViolationType = ConnectionViolation
