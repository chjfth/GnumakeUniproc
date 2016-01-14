@echo off
setlocal enabledelayedexpansion
rem set tmpbatdir=%~dp0%
rem set _gmudir_bs=%tmpbatdir:\GMU-main\umake_cmd\wincmd\=%
REM	_gmudir_bs will result in something like D:\GMU
REM					set _gmudir=%_gmudir_bs:\=/%
set _exdir=%~dp0GMU-examples

set gmuex_11=%_exdir%\common\walkdir\make-all
set gmuex_21=%_exdir%\windows\KeyView2
set gmuex_31=%_exdir%\make-all\all-on-windows\all.msvc

echo ======================================================================
echo Select a directory by entering a number(e.g. 11 will select gmuex_11):
echo ======================================================================
set gmuex
	REM List all env-vars whose name start with gmuex.
echo.

SET /P exid=Enter selection:
set done_exdir=!gmuex_%exid%!

endlocal & (
	set _gmu_exdir=%done_exdir%
)

REM echo %_gmu_exdir%
pushd %_gmu_exdir%

