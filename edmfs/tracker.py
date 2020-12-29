from typing import Dict, Any

class Tracker:
    def __init__(self, name:str):
        self._name:str = name
    
    @property
    def name(self) -> str:
        return self._name

    def on_docked_entry(self, entry:Dict[str, Any]):
        return None