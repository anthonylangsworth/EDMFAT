# Introduction

Elite: Dangerous Minor Faction Activity Tracker (EDMFAT) is an EDMC plug-in that automatically records in-game actions supporting or undermining a minor faction. For example, completing missions for a minor faction will increase that minor faction's influence. Completing missions for other minor factions in the same system will decrease that minor faction's influence.

This plug-in is aimed at **Elite: Dangerous** squadrons that support a minor faction for background simulation (BGS) work. Without the plug-in, players had to manually keep records. This is difficult for new players. It is also immersion-breaking and error prone, even for experienced ones.

Originally intended to support the [Elite Dangerous AU & NZ](https://inara.cz/squadron/687/) squadron and their minor faction [EDA Kunti League](https://inara.cz/galaxy-minorfaction/33400/), the long term goal is to generalize this plug-in into something useful for the broader **Elite: Dangerous** community.

# Installation and Upgrade

Requirements:
1. Install [Elite Dangerous Market Connector (EDMC)](https://github.com/EDCD/EDMarketConnector/wiki/Installation-&-Setup) version 4.0 or later.

To upgrade from an earlier version:
1. Delete the existing EDMFAT plug-in folder, normally found at `%USERPROFILE%\AppData\Local\EDMarketConnector\plugins\EDMFAT` on Windows.
2. Follow the steps under "To install" below.

To install:
1. Download the latest ZIP file under "Releases" at the top right.
2. Copy the ZIP file into your EDMC plug-ins folder, normally `%USERPROFILE%\AppData\Local\EDMarketConnector\plugins` on Windows.
3. Expand the ZIP file. This should create and "EDMFAT" folder with the plug-in files inside it.
4. Restart EDMC if it was already running.

# Use

1. Start EDMC. This is important. If you start EDMC while Elite: Dangerous is running, the plug-in may miss important events.
2. (Optional) Go to "File" -> "Settings", navigate to the "Minor Faction Activity Tracker" tab and change the "Minor Faction" to the one you want to support or undermine. If it does not appear in the list, travel to a system where the faction is present then reopn the preferences dialog. The minor faction is saved and so only needs to be done once. The list of minor factions is not saved.
3. Play **Elite: Dangerous**, supporting or undermining your minor faction. 
4. Minor faction-relevant activity will be captured and appear in the EDMC window. The plug-in tracks completing missions, selling bounty vouchers, selling combat bonds, trade (positive, negative and black market) and selling cartography data. The plug-in does not track failed missions or clean ship kills, which may be added in the future. The plug-in cannot track conflict zones due to limitations with **Elite: Dangerous**. 
5. (Optional) Change the minor faction to support or undermine as per step 2. This can be done at any time. Previous activity is retained.
6. When done, press the "Copy" button to copy your activity to the Windows clipboard.
6. (Optional) Press the "Copy + Reset" button to copy your activity to the Windows clipboard and clear any activity. This can be useful if you want to report activity part way through a session, such as before the daily or weekly tick.
7. Paste it into your squadron's Discord channel or wherever you report activity.

# Limitations

1. The plug-in is not state-aware. For example, the influence of a minor faction in a "War" state is fixed until the war completes. However, this plug-in will still track missions and other activity as normal.
2. The plug-in can only track the work for one minor faction at a time. This may be addressed in the future.
3. The plug-in does not store different minor factions for different commanders. However, many use multiple accounts for minor faction work.
4. The plug-in is not localized. It is English only.
5. This plug-in does not support console players. Sorry. This is a limitation of EDMC.
