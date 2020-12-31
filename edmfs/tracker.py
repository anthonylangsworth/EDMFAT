from typing import Dict, Any
from abc import ABC, abstractmethod

from .state import Station, PilotState, GalaxyState
from .event_processors import EventProcessor, _eventProcessors

class Tracker:
    def __init__(self, minor_faction:str):
        self._minor_faction:str = minor_faction
        self._pilot_state:PilotState = PilotState()
        self._galaxy_state:GalaxyState = GalaxyState()
        self._event_summaries:list = []
        self._activity = ""
    
    @property
    def minor_faction(self) -> str:
        return self._minor_faction

    @property
    def pilot_state(self) -> PilotState:
        return self._pilot_state

    @property
    def galaxy_state(self) -> GalaxyState:
        return self._galaxy_state

    @property
    def activity(self) -> str:
        return self._activity

    def on_event(self, entry:Dict[str, Any]) -> None:
        eventProcessor:EventProcessor = _eventProcessors.get(entry["event"], None)
        if eventProcessor != None:
            event_summaries = eventProcessor.process(entry, self.minor_faction, self.pilot_state, self.galaxy_state)
            if event_summaries:
                self._event_summaries.extend(event_summaries)
                # TODO: Aggregate by system, sum similar entries, etc
                self._activity = "\n".join(str(event_summary) for event_summary in self._event_summaries)
        