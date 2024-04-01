# Release Process

## Prerequisites

1. Download the latest version of the [WiX Toolset](https://wixtoolset.org/releases/) using `dotnet tool install --global wix`.
2. Install the WiX UI extension using `wix extension add -g WixToolset.UI.wixext/4.0.4`.
4. (Optional) Have `signtool.exe` in the PATH and the correct digital certificate in an accessible certificate store.

## Process

1. Update the version in:
    1. `load.py` in the `this.version` field on line 22.
    2. `wix\edmfat.wxs` in the `<Package>` element on line 2 and `<UpgradeVersion>` elements on lines 5 and 6.
2. Run `wix\buildmsi.cmd` to create the MSI.
3. (Optional) Run `wix\signmsi.cmd` to digitally sign the MSI.
4. Install the MSI and test as desired. For reference, the files are installed to `%USERPROFILE%\AppData\Local\EDMarketConnector\plugins\EDMFAT`.
5. Update documentation, such as [README.md](../README.md).
6. Commit the changes and push them to Git Hub.
7. Create a new release.
    1. Set the tag to the version number.
    2. Add release comments as appropriate.
    3. Upload the MSI.
8. Publish the release.
