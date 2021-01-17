from typing import Dict, Any, Set
from abc import ABC, abstractmethod
from itertools import groupby
import logging

from .state import Station, PilotState, GalaxyState
from .event_processors import EventProcessor, _default_event_processors, NoLastDockedStationError, UnknownStarSystemError
from .event_formatters import EventFormatter, _default_event_formatters
from .event_summaries import EventSummary, _default_event_summary_order

class Tracker:
    def __init__(self, minor_factions:iter, logger:logging.Logger = None, event_processors:Dict[str, object] = None,  event_formatters: Dict[str, object] = None, event_summary_order:iter = None):
        self._minor_factions = set(minor_factions)
        self._logger = logger if logger else logging
        self._pilot_state = PilotState()
        self._galaxy_state = GalaxyState()
        self.clear_activity()
        self._event_processors = event_processors if event_processors else _default_event_processors
        self._event_formatters = event_formatters if event_formatters else _default_event_formatters
        self._event_summary_order = tuple(event_summary_order if event_summary_order else _default_event_summary_order)
    
    @property
    def minor_factions(self) -> Set[str]:
        return self._minor_factions
    
    @minor_factions.setter
    def minor_factions(self, value:iter) -> None:
        self._minor_factions = set(value)

    @property
    def pilot_state(self) -> PilotState:
        return self._pilot_state

    @property
    def galaxy_state(self) -> GalaxyState:
        return self._galaxy_state

    @property
    def activity(self) -> str:
        return self._activity

    def clear_activity(self) -> None:
        self._event_summaries = []
        self._activity = ""

    def on_event(self, event:Dict[str, Any]) -> bool:
        new_event_summaries = self._process_event(event)
        activity_updated = False # Consider an Observer pattern or similar
        if new_event_summaries:
            self._event_summaries.extend(new_event_summaries)
            self._activity = self._update_activity(self._event_summaries).rstrip("\n")
            self._logger.info(f"{ event } created { new_event_summaries }")
            activity_updated = True
        return activity_updated

    def _process_event(self, event:Dict[str, Any]) -> list:
        event_processor = self._event_processors.get(event["event"], None)
        result = []
        if event_processor != None:
            try:
                result.extend(event_processor.process(event, self.minor_factions, self.pilot_state, self.galaxy_state))
            except NoLastDockedStationError:
                self._logger.exception(f"Last docked station required for {str(event)}")
            except UnknownStarSystemError as unknown_star_system_error:
                self._logger.exception(f"Unknown star system '{unknown_star_system_error.system}'' required for {str(event)}")
        return result
    
    def _update_activity(self, event_summaries:list) -> str:
        result = ""
        sorted_event_summaries = sorted(sorted(sorted(sorted(event_summaries, key= lambda x: self._event_summary_order.index(type(x).__name__)), key=lambda x: x.supports), key=lambda x: x.system_name), key=lambda x: x.minor_faction)
        for (system_name, minor_faction, supports), event_summaries_by_system in groupby(sorted_event_summaries, key=lambda x: (x.system_name, x.minor_faction, x.supports)):
            result += f"{system_name} - {'PRO' if supports else 'ANTI'} {minor_faction}\n"
            for type_name, system_event_summaries_by_system_and_type in groupby(event_summaries_by_system, key=lambda x: type(x).__name__):
                event_formatter = self._event_formatters.get(type_name, None)
                if event_formatter:
                    result += event_formatter.process(system_event_summaries_by_system_and_type)
            result += "\n"
        return result
        