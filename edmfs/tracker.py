from typing import Dict, Any
from abc import ABC, abstractmethod
from typing import Dict, Any

class EventProcessor(ABC):
    @property
    @abstractmethod
    def eventName(self) -> str:
        pass

    @abstractmethod
    def process(self, entry:Dict[str, Any]) -> None:
        pass
    
# Eventually, move this to an IoC setup
_eventProcessors:Dict[str, EventProcessor] = {
    "location": None,
    "docked": None
}

class Tracker:
    def __init__(self, minor_faction:str):
        self._minor_faction:str = minor_faction
    
    @property
    def minor_faction(self) -> str:
        return self._minor_faction

    def on_entry(self, entry:Dict[str, Any], state:Dict[str, Any]):
        eventProcessor:EventProcessor = _eventProcessors.get(entry["event"], None)
        if eventProcessor != None:
            eventProcessor.process(entry)
        return None

