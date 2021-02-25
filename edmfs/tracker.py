from typing import Dict, Any, Set, Callable, Tuple, Iterable
from abc import ABC, abstractmethod
from itertools import groupby
import logging

from .state import Station, PilotState, GalaxyState, StarSystem
from .event_processors import EventProcessor, _default_event_processors, UnknownPlayerLocationError, UnknownStarSystemError
from .event_formatters import EventFormatter, _default_event_formatters
from .event_summaries import EventSummary, _default_event_summary_order

def _get_dummy_logger():
    logger = logging.getLogger("dummy")
    logger.addHandler(logging.NullHandler())
    return logger


class Tracker:
    def __init__(self, minor_factions:Iterable[str], logger:logging.Logger = None, star_system_resolver: Callable[[int], StarSystem] = None, 
            event_processors:Dict[str, object] = None,  event_formatters: Dict[str, object] = None, event_summary_order:Iterable[str] = None):
        self._minor_factions = set(minor_factions)
        self._logger = logger if logger else _get_dummy_logger()
        self._pilot_state = PilotState()
        self._galaxy_state = GalaxyState(star_system_resolver)
        self.clear_activity()
        self._event_processors = event_processors if event_processors else _default_event_processors
        self._event_formatters = event_formatters if event_formatters else _default_event_formatters
        self._event_summary_order = tuple(event_summary_order if event_summary_order else _default_event_summary_order)
    
    @property
    def minor_factions(self) -> Tuple[str]:
        # Create Tuple to force read-only. Sort to ensure determinism.
        return tuple(sorted(self._minor_factions))
    
    @minor_factions.setter
    def minor_factions(self, value:Iterable) -> None:
        self._minor_factions = set(value)
        self._update_activity()

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
            self._update_activity()
            self._logger.info(f"Minor faction relevant: { event }")
            for event_summary in new_event_summaries:
                self._logger.info(f"Created { event_summary }")
            activity_updated = True
        return activity_updated

    def _process_event(self, event:Dict[str, Any]) -> list:
        event_processor = self._event_processors.get(event["event"], None)
        result = []
        if event_processor != None:
            try:
                result.extend(event_processor.process(event, self.pilot_state, self.galaxy_state))
            except UnknownPlayerLocationError:
                self._logger.exception(f"Player location (station or system) required for {str(event)}")
            except UnknownStarSystemError as unknown_star_system_error:
                self._logger.exception(f"Unknown star system '{unknown_star_system_error.system}' required for {str(event)}")
        return result

    def _update_activity(self) -> None:
        activity = []
        for minor_faction in sorted(self._minor_factions):
            filtered_event_summaries = filter(lambda x: minor_faction in x.pro or minor_faction in x.anti, self._event_summaries)
            sorted_event_summaries = sorted(sorted(sorted(filtered_event_summaries, key= lambda x: self._event_summary_order.index(type(x).__name__)), key=lambda x: minor_faction in x.pro), key=lambda x: x.system_name)
            for (system_name, supports), event_summaries_by_system in groupby(sorted_event_summaries, key=lambda x: (x.system_name, minor_faction in x.pro)):
                activity.append(f"{system_name} - {'PRO' if supports else 'ANTI'} {minor_faction}")
                for type_name, system_event_summaries_by_system_and_type in groupby(event_summaries_by_system, key=lambda x: type(x).__name__):
                    event_formatter = self._event_formatters.get(type_name, None)
                    if event_formatter:
                        activity.extend(event_formatter.process(system_event_summaries_by_system_and_type))
                activity.append("")
        self._activity = "\n".join(activity).rstrip("\n")
        