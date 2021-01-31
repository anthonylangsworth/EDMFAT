set dest=%userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT
copy %dest%\settings.json %temp%
rd /s /q %dest%
mkdir %dest%
xcopy /y load.py %dest%
mkdir %dest%\edmfs
xcopy /s /y edmfs\*.py %dest%\edmfs 
copy %temp%\settings.json %dest%
