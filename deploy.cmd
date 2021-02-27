set dest=%userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT
copy %dest%\settings.json %temp% || goto error
rd /s /q %dest% || goto error
mkdir %dest% || goto error
xcopy /y load.py %dest% || goto error
xcopy /y web_services.py %dest% || goto error
mkdir %dest%\edmfs || goto error
xcopy /s /y edmfs\*.py %dest%\edmfs  || goto error
copy %temp%\settings.json %dest% || goto error

goto end

:error
echo Error %errorlevel%
exit /b %errorlevel%

:end