import json

class JobLogsData:
    def __init__(self, logs: str) -> None:
        self.logs = logs

    def to_json(self):
        return {
            "logs": self.logs
        }
