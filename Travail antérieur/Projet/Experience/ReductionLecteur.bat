@echo off
for /f "tokens=2" %%a in ('tasklist /nh /fi "imagename eq wmplayer.exe"') do (
    set "PID=%%a"
    goto :next
)
:next
taskkill /f /pid %PID%