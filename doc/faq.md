# Frequently Asked Questions

### 1. The activity shown is incorrect. For example, a mission influence reward is wrong. How do I fix this?

Unfortunately, **Elite: Dangerous** occasionally records incorrect mission influence values. See the [discussion on missions](missions.md).

Assuming the problem is not due to known issues with missions, please either:
1. Direct message me via Discord (preferred for those in my squadron), 
2. [Raise an issue on Github](https://github.com/anthonylangsworth/EDMFAT/issues) or
3. Contact me via social media links in [my Github profile](https://github.com/anthonylangsworth).

I will need:
1. The relevant journal file(s) from the play session. These are usually found in `%userprofile%\Saved Games\Frontier Developments\Elite Dangerous\` in the form of `Journal.YYYYMMDDHHmmSS.01.log` where YYYYMMDDHHmmSS is a date and time in reverse order.
2. The minor faction(s) being supported or undermined.
3. An explanation of what should have happened. For example, if sold cartography data does not appear, please tell me where you sold it (the station or settlement) and when (the rough game time).

### 2. The EDMC plug-in is not loading or not working correctly. How do I fix this?

Please ensure the latest version of EDMC is installed and working correctly. This plug-in will not work with versions before 4.0.

While EDMC is running, check its log file, usually found at `%temp%\EDMarketConnector.log`. If you have difficulty reading the log (it is designed for developers, after all), please reach out to me as per the instructions above. Please attach the relevant log file(s), describe what you were trying to do and what actually happened.

### 3. How do I change the minor faction(s) I want to support?

To change the minor faction(s):
1. Open the `File` menu -> `Settings` menu item. This opens the settings dialog.
2. Navigate to the "Minor Faction Activity Tracker" tab. This shows the settings for this plug-in.
3. Select or deselect the desired minor faction(s) by clicking rows in the table. 

The plug-in learns about new minor factions as you travel to new systems. If the minor faction you want to support or undermine a faction not in the list:
1. Press `OK` to close the dialog. Keep EDMC running.
2. In **Elite: Dangerous**, travel to a system where the minor faction is present.
3. Follow the steps above to reopen the settings dialog then select the desired minor faction(s). 

This plug-in saves the selected minor factions. If you exit EDMC and start it later, you do not need to reselect minor faction(s) unless you want to change them. This plug-in does not save the list of minor factions in the settings dialog.

### 4. Will this plug-in work with the Odyssey expansion?

Yes. The plug-in includes support for organic data, although its BGS relevance is uncertain. Combat bonds earned on foot are treated the same as ship-earned combat bonds.

The plug-in intentionally excludes any events from "beta versions of **Elite: Dangerous**, as per the EDMC API. Presumably, any alphas or betas will use separate universes to the main universe. Any BGS activity there will likely be separate to the main universe.

### 5. I accidentally did a mission that hurt my minor faction. Help!

Don't Panic! This commonly happens when you do not check a mission's target faction. Treat it as a learning experience. You can always edit it out when copying your activity into your squadron Discord (or however you report your activity).

### 6. Why doesn't the plug-in automatically update Discord or upload this to a website? Why do I have to copy and paste it?

I am happy to add this as a feature if there is sufficient demand. However, I have intentionally taken a minimalist approach to the plug-in. I prefer simple, testable and understandable over fully-featured but complex.

Copying allows players to annotate activity. For example, they can explain why actions are relevant or apparent anti-minor faction activity.

Copying allows players to edit or remove irrelevant activity. Some may think this reduces the trustworthiness of EDMFAT's results. However, ignoring this potential change, not all data sent to Discord or a website is automatically trustworthy.
