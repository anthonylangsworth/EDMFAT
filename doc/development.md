This a scratch pad to record development-specific details, keeping them separate from user documentation.

# Development Principles

1. Ease of Use. For example, "Copy + Reset" instead of Reset button. Avoid non-game abbreviations in activity.
2. Try to follow in-game values where possible. The journal file sometimes makes that difficult with [missions](doc/missions.md).
3. KISS (Keep It Simple, Stupid!). For example, eschew plug-ins or dependencies unless necessary.

# TODO

1. Looking up system if not found, e.g. handing in a wing mission. Also solves problem of EDMC started after mission acceptance. Consider the EDMC API.
2. Tracking killing clean ships
3. Add troubleshooting FAQs, e.g. %userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT, %TEMP%\EDMarketConnector.log
4. Automating the installation, e.g. a WIX MSI.
5. (low) Evangelizing the plug-in.
6. (low) Reformat the files to be PEP8 compliant.

# References

1. EDMC Plug-in details: https://github.com/EDCD/EDMarketConnector/blob/main/PLUGINS.md
2. Elite Dangerous Journal File format: http://hosting.zaonce.net/community/journal/v27/Journal-Manual_v27.pdf