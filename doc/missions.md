# Mission Challenges

Unfortunately, the mission influence results shown by this plug-in are sometimes incorrect. When the **Elite: Dangerous** game UI gives the player a choice of mission rewards, each choice contains a single influence value. However, the journal file and, therefore, EDMC events often give (1) different influence values for the source (giving) and optional target minor faction or (2) incorrect values. This inaccuracy is a known issue with **Elite: Dangerous**.

This plug-in assumes the values shown in the in-game UI are correct. Therefore, this plug-in looks for the highest influence value of (1) the influence value given when the mission is accepted, (2) the source minor faction influence change or (3) the optional target minor faction influence change. Anecdotally, this matches the in-game UI influence value about ninety percent of the time. When it is incorrect, it is usually out by a single "+".

Given this inaccuracy, are the plug-in's mission results trustworthy? It depends on how you use the results.

Reliably accurate mission results do not give background simulation (BGS) predictability. The inner workings of the BGS are poorly understood, undocumented and subject to change. Other than a rough correlation, the relationship between a system's population and influence change is unknown. The conversion of influence pluses ("+"s) to other influence impacting actions like selling bounties or cartography data is poorly estimated. Daily influence caps per player and minor faction exist but are unknown. Some minor faction states affect influence changes. For example, "War" and "Civil War" states freeze a minor faction's influence until the conflict ceases. The "Boom" state increases the influence impact of trade missions. Even if influence could be counted accurately other factors can impact the influence gain or loss like power play or other players.

If you want a completely accurate mission influence record, such as for detailed experiments into missions and influence changes, you will need to record available and completed missions manually. I know of no way to programmatically get accurate mission information. If you know of a more accurate source or algorithm, I am very interested to know more. Please contact me via [social networking links in my github profile](https://github.com/anthonylangsworth) or [raise an issue](https://github.com/anthonylangsworth/EDMFAT/issues)!

If you want to compete with other players to determine who helps or hinders more, influence from missions completed in the short term (for example, a typical play session of a few hours) is often constrained by the randomly generated missions and less by player skill. While players with higher reputation and combat/exploration/trade ranks tend to get higher rewarding missions, this is not guaranteed. Tracking comparative effort may be possible over extended periods (for example, months) but the plug-in does not currently retain tracked activity after exiting EDMC.

Therefore, the recommended use for the mission influence results (and the plug-in generally) is a guide. It helps squadron members or other players understand where you have focused your time. They can then assist, if more effort is needed, or work elsewhere, if not. Occasional extra or omitted influence "+"s will not affect that.

Similarly, this plug-in simplifies minor faction missions into increasing (PRO) or decreasing (ANTI) a minor faction's influence. More accurately, four types of missions impact a minor faction's influence:
1.	Direct support: Increases the minor faction's influence, such as completing a mission for that faction.
2.	Direct undermine: Decrease the minor faction's influence, such as an assassination mission destroying a ship owned by that minor faction.
3.	Indirect support: Decrease another minor faction's influence in that system. This effectively boosts the influence of all other minor factions in that system. It is a smaller influence increase than direct support.
4.	Indirect undermine: Increase another minor faction's influence in that system. This effectively decreases the influence of all other minor factions in that system. It is a smaller influence decrease than direct undermine.

Have fun and fly safely from CMDR Akton!

# Known Mission Issues

1. This plug-in may not track completing shared wing missions where the player has not visited the system the mission was given (accepted).
2. This plug-in may not track completing missions if (1) the mission was accepted when EDMC was not running or (2) EDMC was restarted since the mission was accepted.
