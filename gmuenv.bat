@set _gmu_DIR_ROOT_bs_=%~dp0
@pushd %~dp0
@for /F usebackq %%i IN (`%~dp0MinGW2\bin\pwd.exe`) DO set gmu_DIR_ROOT=%%i
@popd
@REM If full path of this .bat is D:\some\path\gmuenv.bat, resulting gmu_DIR_ROOT=D:/some/path
