# Contributing

This a scratch pad to record development-specific details, keeping them separate from user documentation.

## Development Principles

Development uses the following principles:
1. **Ease of Use:** This is a game played by people from a variety of backgrounds, often for long periods. Require as little thought as possible from the user. For example, avoid non-game abbreviations in activity. Be forgiving, such as using a "Copy + Reset" button to clear activity instead of a "Reset" button. 
2. **In-Game is Correct:** Assume influence and totals shown in the in-game UI are correct. The journal file sometimes makes that difficult with [missions](doc/missions.md).
3. **Simple Design:** Follow good design principles and keep the plug-in design as simple as possible. For example, eschew plug-ins or dependencies unless necessary.

## TODO

A rough backlog:
1. Looking up system if not found, e.g. handing in a wing mission. Also solves problem of EDMC started after mission acceptance. Consider the EDMC API.
2. Tracking killing clean ships
3. Add troubleshooting FAQs, e.g. %userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT, %TEMP%\EDMarketConnector.log
4. Automating the installation, e.g. a WIX MSI.
5. (low) Evangelizing the plug-in.
6. (low) Reformat the files to be PEP8 compliant.

## References

1. EDMC Plug-in details: https://github.com/EDCD/EDMarketConnector/blob/main/PLUGINS.md
2. Elite Dangerous Journal File format: http://hosting.zaonce.net/community/journal/v27/Journal-Manual_v27.pdf