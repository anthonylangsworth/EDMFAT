# What is it?

Elite: Dangerous Minor Faction Activity Tracker (EDMFAT) automatically records game actions that affect a minor faction like selling bounties or completing missions. It is aimed at Elite: Dangerous squadrons that support a minor faction for background simulation work.

Originally intended to support the "Elite Dangerous AU & NZ" squadron and their minor faction "EDA Kunti League", the goal is to generalize this into something useful for the broader Elite: Dangerous community.

# Installation

Requirements:
1. Elite Dangerous Market Connector (EDMC), installed as per https://github.com/EDCD/EDMarketConnector/wiki/Installation-&-Setup. This plug-in requires version 4.0 or later.
2. This plug-in does not support console players. Sorry. This is a current limitation of EDMC.

To install:
1. Download the latest ZIP file under "Releases" at the top right.
2. Copy the ZIP file into your EDMC plug-ins folder, normally `%USERPROFILE%\AppData\Local\EDMarketConnector\plugins` on Windows.
3. Expand the ZIP file. This should create and "EDMFAT" folder with the plug-in files inside it.
4. Restart EDMC if it was already running.

# Use

1. Start EDMC. This is important. If you start EDMC while Elite: Dangerous is running, the plug-in may miss important events.
2. (Optional) Go to "File" -> "Preferences", navigate to the "Minor Faction Activity Tracker" tab and change the "Minor Faction" to the one you want to support or undermine. This name must EXACTLY match that in game. I recommend copying it from Inara or similar to be certain. This is saved and so only need to be done once.
3. Play Elite: Dangerous, supporting your minor faction. 
4. Minor faction-relevant activity will be captured and appear in the EDMC window. It tracks missions, selling bounty vouchers, selling combat bonds, trade (positive, negative and black market) and selling cartography data.
5. When done, press the "Copy" button to copy the activity to the clipboard.
6. Paste it into your team's Discord channels or wherever you report activity.

Limitations:
1. The plug-in does not store different minor factions for different commanders. However, many use multiple accounts for minor faction work.
2. The plug-in is not localized.
