import json
import os

class StateStore:
    def __init__(self, path="state.json"):
        self.path = path
        self.processed = set()
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.processed = set(data.get("processed", []))

    def is_processed(self, message_id: int) -> bool:
        return message_id in self.processed

    def add(self, message_id: int):
        self.processed.add(message_id)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"processed": list(self.processed)}, f, indent=2)
