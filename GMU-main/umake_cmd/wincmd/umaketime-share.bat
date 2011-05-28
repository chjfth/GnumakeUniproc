@echo off
setlocal
:Thanks to jeb from http://stackoverflow.com/questions/4487100/how-can-i-use-a-windows-batch-file-to-measure-the-performance-of-console-applicat
set "startTime=%time%"

call %~dp0umake-share.bat %*

set "stopTime=%time%"
call :timeDiff diff startTime stopTime
set /A _sec_=%diff% / 1000
set /A _msec_=%diff% %% 1000
echo Gmu seconds used: %_sec_%.%_msec_%
goto :eof

:timeDiff
setlocal
call :timeToMS time1 "%~2"
call :timeToMS time2 "%~3"
set /a diff=time2-time1
(
  ENDLOCAL
  set "%~1=%diff%"
  goto :eof
)

:timeToMS
::### WARNING, enclose the time in " ", because it can contain comma seperators
SETLOCAL EnableDelayedExpansion
FOR /F "tokens=1,2,3,4 delims=:,.^ " %%a IN ("!%~2!") DO (
  set /a "ms=(((30%%a%%100)*60+7%%b)*60+3%%c-42300)*1000+(1%%d0 %% 1000)"
)
(
  ENDLOCAL
  set %~1=%ms%
  goto :eof
)
