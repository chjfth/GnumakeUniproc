@echo off
setlocal
REM List GMU variables, were it launched from this GMU directory

set tmpbatdir=%~dp0%
set gmu_DIR_ROOT_bs=%tmpbatdir:\GMU-main\umake_cmd\wincmd\=%
set gmu_DIR_ROOT=%gmu_DIR_ROOT_bs:\=/%

call %gmu_DIR_ROOT_bs%\_gmuenv.bat

set gmu_
set gmp_ 2>NUL
set gmi_ 2>NUL
set gms_ 2>NUL
set gv1 2>NUL
set gv2 2>NUL

: Without 2>NULL , CMD will say 'Environment variable gmi not defined', when no env-var starts with gmi.
