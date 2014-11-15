@echo off
setlocal

set tmpbatdir=%~dp0%
set gmu_DIR_ROOT_bs=%tmpbatdir:\GMU-main\umake_cmd\wincmd\=%
set gmu_DIR_ROOT=%gmu_DIR_ROOT_bs:\=/%

call %gmu_DIR_ROOT_bs%\_gmuenv.bat

set gfdir=gf

IF not "%~1" == "" (
	set gfdir=%~1
)

echo Removing directory "%gfdir%"
rm -fr "%gfdir%"

if %ERRORLEVEL% == 0 (
	echo Done.
)
