import json
from datetime import datetime


class BaseModel:

    def __init__(self, created_at, updated_at):
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = 0

    def to_json_object(self):
        return json.loads(self.to_json_str())

    def to_json_str(self):
        return json.dumps(self,
                          default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else o.__dict__,
                          sort_keys=True, indent=4)
