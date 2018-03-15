@echo off

REM If you want to call umake.bat from a wrapper script and you want to know
REM the exit code(success or failure) of umake.bat, you MUST set an env-var
REM    TEEBAT_WRAPPER_EXISTED=1 
REM before calling umake.bat. To make life a little easier, you can just 
REM this umake1.bat .

set TEEBAT_WRAPPER_EXISTED=1

call %~dp0umake-share.bat %*
