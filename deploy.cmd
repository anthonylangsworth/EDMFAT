set dest=%userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT
mkdir %dest%
xcopy /y load.py %dest%
mkdir %dest%\edmfs
xcopy /e /y edmfs %dest%\edmfs 