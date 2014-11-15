@echo off
set gmu_DIR_ROOT_bs=%~dp0
set gmu_DIR_ROOT_bs=%gmu_DIR_ROOT_bs:~0,-1%

set gmu_DIR_ROOT=%gmu_DIR_ROOT_bs:\=/%
:	If full path of this .bat is D:\some\path\gmuenv.bat, result is gmu_DIR_ROOT=D:/some/path

REM More env-vars below appended by GMU installer from _gmuenv.bat
REM You can customize GMU vars by calling your own .bat before or after _gmuenv.bat .

REM call %gmu_DIR_ROOT_bs%\my-env1.bat

call %gmu_DIR_ROOT_bs%\_gmuenv.bat

REM call %gmu_DIR_ROOT_bs%\my-env2.bat

REM doskey lgmv=set gmu_ $T set gmp_ $T set gmi_ 2$g NUL $T set gms_ 2$g NUL
:	Without 2>NULL , CMD will say 'Environment variable gmi not defined', when no env-var starts with gmi.
:   [2014-11-15] Weird output executing lgmv with doskey, prompt string AND output mixed.

echo.
echo GnumakeUniproc %gmu_ver% environment variables set OK.
echo To see what variables are set, type command 'lgmv' .
echo.
