This a scratch pad to record development-specific details, keeping them separate from user documentation.

# Development Principles

1. Ease of Use. For example, "Copy + Reset" instead of Reset button. Avoid non-game abbreviations in activity.
2. Try to follow in-game values where possible. The journal file sometimes makes that unclear.
3. Keep the code simple. For example, eschew plug-ins or dependencies unless necessary.

# TODO

1. Looking system if not found, e.g. handing in a wing mission. Also solves problem of EDMC started after mission acceptance.
2. Killing clean ships
3. Add troubleshooting FAQs, e.g. %userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT, %TEMP%\EDMarketConnector.log

# Challenges with missions

Unfortunately, the mission influence results shown by this plug-in are sometimes incorrect. When the **Elite: Dangerous** game UI gives the player a choice of mission rewards, each choice contains a single influence value. However, the journal file and, therefore, EDMC events often gives (1) different values for the source (giving) and optional target minor faction or (2) omits them.

This inaccuracy is a known issue with the values written by the **Elite: Dangerous** game client to the journal files. EDMC reads these values and passes them to plug-ins like this one. I know of no other reliable way to get details of completed missions programmatically.

This plug-in assumes the values shown in the in-game UI are correct. Therefore, this plug-in looks for the highest influence value of (1) the influence value given when the mission is accepted, (2) the source minor faction infuence change or (3) the optional target minor faction influence change. Anecdotaly, this reflects the in-game UI influence value about ninety percent of the time. When it is incorrect, it is normally out by a single "+".

Given this inaccuracy, are the plug-in's mission results trustworthy? It depends on how you use the results. 

Completely accurate missions results do not give background simulation (BGS) predictability. The inner workings of the BGS are poorly understood, undocumented and subject to change. Other than a rough correlation, the relationship between a system's population and influence change is unknown. The conversion of influence pluses ("+"s) to other influence impacting actions like selling bounties or cartography data is poorly estimated. Daily influence caps per player and minor faction exist but are unknown. Certain minor faction states affect influence changes. For example, "War" and "Civil War" states freeze a minor faction's influence until the conflict ceases. The "Boom" state increases the influence impact of trade missions. Even if influence could be counted accurately other factors can impact the influence gain or loss like power play or other players.

If you want a completely accurate mission influence record, such as for detailed experiments into missions and influence changes, I know of no way to programmatically get this information. If you know of a more accurate source or algorithm, I would by very interested to know more. Until then, you will need to manually record available and completed missions. 

If you want to complete with other players to determine who helps or hinders more, influence available and completed in the short term (e.g. a normal play session of a few hours) is often constrained by the missions randomly generated. While players with higher reputation and combat/exploration/trade ranks tend to get higher rewarding missions, this is not guaranteed. This may be possible over a longer period (e.g. months) but the plug-in does not currently retain the tracked activity.

Therefore, the recommended use for the mission influence results (and the plug-in generally) is a guide. It helps squadron members or other players understand where you have focused your time. They can then assist, if more effort is needed, or work elsewhere, if not. An occasional extra or omitted influence "+" will not affect that.

Similarly, this plug-in simplifies minor faction related work into increasing (PRO) or decreasing (ANTI) a minor faction's influence. More accurately, there are four types of missions that impact a minor faction's influence:
1. Direct support: Increases the influence of that minor faction, such as completing a mission for that faction.
2. Direct undermine: Decrease the influence of that minor faction, such as an assassination mission against a ship for that faction.
3. Indirect support: Decrease the influence of another minor faction in that system. This effectively boosts the influence of all other minor factions in that system. 
4. Indirect undermine: Increase the influence of another minor faction in that system. This effectively decreases the influence of all other minor factions in that system. 

# References

1. EDMC Plug-in details: https://github.com/EDCD/EDMarketConnector/blob/main/PLUGINS.md
2. Elite Dangerous Journal File format: http://hosting.zaonce.net/community/journal/v27/Journal-Manual_v27.pdf
