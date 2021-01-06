# What is it?

Elite: Dangerous Minor Faction Activity Tracker (EDMFAT) is an EDMC plug-in that automatically records in-game actions supporting or undermining a minor faction. For example, completing missions for a minor faction will increase that minor faction's influence. Completing missions for other minor factions in the same system will decrease that minor faction's influence.

This plug-in is aimed at **Elite: Dangerous** squadrons that support a minor faction for background simulation (BGS) work. Without the plug-in, players hd to manually keep records. This is difficult for new players. It is also immersion-breaking and error prone, even for experienced ones.

Originally intended to support the "Elite Dangerous AU & NZ" squadron and their minor faction "EDA Kunti League", the long term goal is to generalize this into something useful for the broader **Elite: Dangerous** community.

# Installation

Requirements:
1. Elite Dangerous Market Connector (EDMC), installed as per https://github.com/EDCD/EDMarketConnector/wiki/Installation-&-Setup. This plug-in requires version EDMC 4.0 or later.

To install:
1. Download the latest ZIP file under "Releases" at the top right.
2. Copy the ZIP file into your EDMC plug-ins folder, normally `%USERPROFILE%\AppData\Local\EDMarketConnector\plugins` on Windows.
3. Expand the ZIP file. This should create and "EDMFAT" folder with the plug-in files inside it.
4. Restart EDMC if it was already running.

# Use

1. Start EDMC. This is important. If you start EDMC while Elite: Dangerous is running, the plug-in may miss important events.
2. (Optional) Go to "File" -> "Preferences", navigate to the "Minor Faction Activity Tracker" tab and change the "Minor Faction" to the one you want to support or undermine. This name must EXACTLY match the in-game name. I recommend copying it from Inara or similar to be certain. This is saved and so only needs to be done once.
3. Play Elite: Dangerous, supporting or undermining your minor faction. 
4. Minor faction-relevant activity will be captured and appear in the EDMC window. The plug-in tracks missions, selling bounty vouchers, selling combat bonds, trade (positive, negative and black market) and selling cartography data. The plug-in cannot track conflict zones due to limitations with Elite: Dangerous.
5. When done, press the "Copy" button to copy the activity to the Windows clipboard.
6. Paste it into your squadron's Discord channels or wherever you report activity.

Limitations:
1. The plug-in is not state-aware. For example, the influence of a minor faction in a "War" state is fixed until the war completes. However, this plug-in will still track missions and other activity as normal.
2. The plug-in can only track the work for one minor faction at a time. This is primarily a user interface limitation at this time.
3. The plug-in does not store different minor factions for different commanders. However, many use multiple accounts for minor faction work.
4. The plug-in is not localized.
5. This plug-in does not support console players. Sorry. This is a limitation of EDMC.
