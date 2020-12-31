from typing import Dict, Any
from abc import ABC, abstractmethod

from .state import Station, PilotState, GalaxyState
from .event_processor import *

# TODO: move this to an IoC setup
_eventProcessors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor()
}

class Tracker:
    def __init__(self, minor_faction:str):
        self._minor_faction:str = minor_faction
        self._pilot_state:PilotState = PilotState()
        self._galaxy_state:GalaxyState = None
    
    @property
    def minor_faction(self) -> str:
        return self._minor_faction

    @property
    def pilot_state(self) -> PilotState:
        return self._pilot_state

    @property
    def galaxy_state(self) -> GalaxyState:
        return self._galaxy_state

    def on_event(self, entry:Dict[str, Any]) -> None:
        eventProcessor:EventProcessor = _eventProcessors.get(entry["event"], None)
        if eventProcessor != None:
            eventProcessor.process(entry, self.minor_faction, self.pilot_state, self.galaxy_state)
        #TODO: Store return value then summarize using EventSummarizers