# Contributing and Development

## Contributing

Contributions are welcome. A rough process:
1. Please contact me first to discuss new features. You can find my contact details under [my GitHub profile](https://github.com/anthonylangsworth).
2. Create a pull request early, communicating to others what you are working on and allowing collaboration.
3. I will deny pull requests without adequate automated tests.

Guidelines:
1. The high-level design is a bit complex at first but is vital to isolating change and keeping it open. The design is a simple event stream architecture. Specifically:
    1. `load.py` abstracts EDMC from the rest of the plug-in. It handles UI and saving/loading configuration. Except for journal file entries, no other file should depend on any EDMC code or details and vice versa.
    2. `tracker.py` abstracts the logic from EDMC into a separate, reusable module. This file maintains state of the pilot (`pilot_state`) and the galaxy (`galaxy_state`) between entries. However, event processors, event summaries and event formatters (see below) perform the actual work. Theoretically, one could swap the plug-in's logic replacing the default event processors, summaries and formatters. One example is a mining or trading plug-ins, similar to what ED Discovery does.
    3. `event_processors.py` contains code that acts upon journal entries (sometimes called events). Event processors either (1) save changes in the state of the pilot (e.g. accepting a mission, docking at a station) or galaxy (e.g. jumping to a new system) or (2) record minor faction activity. One event processor handles one journal entry type or related types.
    4. `event_summaries.py` contains minor faction influence relevant occurrences created by event processors then rendered human-readable by event formatters. These are anaemic (contain no business logic). These should store the minimum information needed.
    5. `event_formatters.py` contains code to make event summaries human-readable. Any localization code should go here. One event formatter usually handles one event summary type.
    6. `state.py` contains code to store details about the **Elite: Dangerous** universe like missions and stations. These are also anaemic excepting resolving star systems.
    7. `resolvers.py` contains calls to EDSM and potentially other sources to resolve data not in entries.
2. I will deny pull requests that only reformat code. PEP8 format is ideal.

## Development Principles

Development uses the following principles:
1. **In-game is correct:** Assume influence and totals shown in the in-game UI are correct, notwithstannding the [problems with missions](missions.md).
2. **Do one thing well:** Conceivably, this plug-in could advise pilots on effective and ineffective ways of increasing or decreasing influence. A website for each squadron could centrally control minor faction(s) to support. The plug-in could automatically post results to a Discord channel. However, this plug-in achieves 80% of the value by merely tallying relevant activity. 
3. **Ease of use:** Require as little thought as possible from the user. For example, avoid non-game abbreviations in activity. Be forgiving, such as using a "Copy + Reset" button to clear activity instead of a "Reset" button. 
4. **Simple, SOLID design:** Follow good design principles (e.g. SOLID) and keep the plug-in design as simple as possible. For example, eschew plug-ins or dependencies unless necessary. Only store as much state or information as the plug-in needs.
5. **Automated testing:** Apart from `load.py`, automate the plug-in's testing. For example, the activity should be deterministic, having a defined sort order. The design splits functionality into small, isolated, easily testable portions.

## Release Process

See [releasing](releasing.md).

## References

1. EDMC Plug-in details: https://github.com/EDCD/EDMarketConnector/blob/main/PLUGINS.md
2. Elite Dangerous Journal File format: http://hosting.zaonce.net/community/journal/v31/Journal_Manual_v31.pdf
3. BGS Overview from Frontier: https://customersupport.frontier.co.uk/hc/en-us/articles/4405440213010-What-is-the-Background-Simulation-and-how-does-it-work-
