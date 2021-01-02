set dest=%userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT
rd /s /q %dest%
mkdir %dest%
xcopy /y load.py %dest%
mkdir %dest%\edmfs
xcopy /e /y edmfs %dest%\edmfs 