from typing import Dict, Any, Tuple, Optional


class InvalidUsage(Exception):
    
    status_code = 400

    def __init__(self, messages: str, status_code: Optional[int] = None, payload: Optional[Tuple[str, Any]] = None):
        Exception.__init__(self)
        self.messages = messages
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> Dict[str, Any]:
        res = dict(self.payload or ())
        res['messages'] = self.messages
        return res