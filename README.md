# What is it?

Elite: Dangerous Minor Faction Activity Tracker (EDMFAT) automatically records game actions that affect a minor faction like selling bounties or completing missions. It is aimed at Elite: Dangerous squadrons that support a minor faction for background simulation work.

Originally intended to support the "Elite Dangerous AU & NZ" squadron and their minor faction "EDA Kunti League", the goal is to generalize this into something useful for the broader Elite: Dangerous community.

# Installation

Requirements:
1. Elite Dangerous Market Connector (EDMC), installed as per https://github.com/EDCD/EDMarketConnector/wiki/Installation-&-Setup. This plug-in requires version 4.0 or later due to the use of Python 3.7.
2. This plug-in does not support console players. Sorry. This is a current limitation of EDMC.

To install:
1. Download the latest ZIP file under "Releases" at the top right.
2. Copy the ZIP file into your EDMC plug-ins folder, normally `%USERPROFILE%\AppData\Local\EDMarketConnector\plugins`.
3. Expand the ZIP file. This should create and "EDMFAT" folder with the plug-in files inside it.
4. Restart EDMC if it was already running.

# Use

1. Start EDMC. This is important. If you start EDMC while Elite: Dangerous is running, the plug-in may miss important events.
2. Play Elite: Dangerous, supporting your minor faction. 
3. Minor faction-relevant activity will be captured and appear in the EDMC window.
4. When done, press the "Copy" button to copy the activity to the clipboard.
5. Paste it into your team's Discord channels or wherever you report activity.

NOTE:
1. EDMFAT is currently hard coded to the minor faction "EDA Kunti League" minor faction. Eventually, the user will be allowed to change it.
2. The current version is limited to selling bounties, combat bonds and cartography only. Future versions will add trade and missions.
