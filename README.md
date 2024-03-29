[![Github All Releases](https://img.shields.io/github/downloads/anthonylangsworth/EDMFAT/total.svg)]()
![Tests](https://github.com/anthonylangsworth/EDMFAT/actions/workflows/main.yml/badge.svg)

# Introduction

Elite: Dangerous Minor Faction Activity Tracker (EDMFAT) is an EDMC plug-in that automatically records in-game actions supporting or undermining minor factions. For example, completing missions for a minor faction will increase that minor faction's influence. Completing missions for other minor factions in the same system will decrease that minor faction's influence. A busy session may give the following:

![Sample EDMFAT Screenshot](doc/EDMFAT.png)

EDMFAT is aimed at players in **Elite: Dangerous** squadrons that support a minor faction for background simulation (BGS) work. It aims to:
1. Reduce manual record keeping. Manually tracking tasks is difficult for new players. It is also immersion-breaking and error-prone, even for experienced ones.
2. Educate players by highlighting activity that supports or undermines minor factions. 

EDMFAT was initially developed to support the [Elite Dangerous AU & NZ](https://inara.cz/squadron/687/) squadron and their minor faction [EDA Kunti League](https://inara.cz/galaxy-minorfaction/33400/), hence EDA Kunti League being the default minor faction.

Fly safe, commanders, from CMDR Akton!

# Installation and Upgrade

Requirements:
1. Install [Elite Dangerous Market Connector (EDMC)](https://github.com/EDCD/EDMarketConnector/wiki/Installation-&-Setup) version 5.0 (Odyssey release) or later.

To install or upgrade:
1. If upgrading, `Copy` any activity you want to report, just in case.
2. Download the MSI file for the latest release [Releases](https://github.com/anthonylangsworth/EDMFAT/releases) at the top right. You may get a warning saying it is potentially harmful. Please ignore these warnings.
3. Run the MSI. This installs the plug-in, upgrading if an earlier version is present. Running the MSI does not require local administrative privileges.
4. Restart EDMC if it was already running.

To remove or uninstall:
1. Stop EDMC if it is running.
2. Run "Add or Remove Programs" from the Windows Start menu.
3. Select "Elite: Dangerous Minor Faction Activity Tracker (EDMFAT)" then press "Uninstall".

# Use

1. Start EDMC. If you start EDMC while **Elite: Dangerous** is running, the plug-in may miss important events.
2. (Optional) Go to the "File" -> "Settings" menu, navigate to the "Minor Faction Activity Tracker" tab and select the minor faction(s) you want to support or undermine from the list. If they do not appear in the list, travel to a system where the faction is present then reopen the Settings dialog. EDMFAT saves the selected minor factions when EDMC shuts down and so only needs to be done once. EDMFAT does not save the list of minor factions.
3. Play **Elite: Dangerous**, supporting or undermining your minor faction(s). 
4. EDMFAT captures minor faction-relevant activity in the main EDMC window. EDMFAT tracks [completing missions](doc/missions.md), redeeming bounty vouchers (but not at interstellar factors), redeeming combat bonds (including at interstellar factors and carriers), trade (positive, negative and black market), selling cartography data, selling organic data, failed missions and clean ship kills. EDMFAT cannot track conflict zone wins and losses due to  **Elite: Dangerous** limitations. 
5. (Optional) Change the minor faction(s) to support or undermine as per step 2. This can be done at any time. The plug-in recalculates any previous activity.
6. When done, press the `Copy` button to copy your activity to the Windows clipboard.
6. (Optional) Instead of pressing the `Copy` button, press the `Copy + Reset` button to copy your activity to the Windows clipboard and clear any activity. Do this at the end of a session when reporting activity.
7. Paste it into your squadron's Discord channel or wherever you report activity.

Read the [FAQ](doc/faq.md) for more details.

See [LICENSE](LICENSE) for the license.

# Limitations

1. **Elite: Dangerous** limits the [missions](doc/missions.md) EDMFAT can track.
2. EDMFAT cannot track conflict zone wins and losses because **Elite: Dangerous** does not report them. It reports combat bonds as the best estimate, even when sold at an interstellar factors or carrier, and corrects them for any broker percentage.
3. EDMFAT is not state-aware to keep it simple. For example, the influence of a minor faction in a "War" state is fixed until the war completes. However, this plug-in will still track missions and other activity as normal.
4. EDMFAT does not store different minor factions for different commanders. This is intentional because many use multiple accounts for minor faction work to bypass daily caps.
5. EDMFAT is not localized. It is English only. Localization assistance is appreciated!
6. EDMFAT does not support console players. Sorry. This is a limitation of EDMC.

See the [issues page](https://github.com/anthonylangsworth/EDMFAT/issues), too.

# Contributing and Development

Bug reports and suggestions are welcome! Please read the [FAQ](doc/faq.md) for details.

See [Contributing](doc/contributing.md) if you want to help with development.

