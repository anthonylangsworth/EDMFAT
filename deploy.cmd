set dest=%userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT
copy %dest%\settings.json %temp%
rd /s /q %dest%
mkdir %dest% || goto error
xcopy /y load.py %dest% || goto error
xcopy /y edmfat_web_services.py %dest% || goto error
mkdir %dest%\edmfs || goto error
xcopy /s /y edmfs\*.py %dest%\edmfs  || goto error
copy %temp%\settings.json %dest%

goto end

:error
echo Error %errorlevel%
exit /b %errorlevel%

:end