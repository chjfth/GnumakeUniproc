@echo off
: List GMU variables
set gmu_
set gmp_
set gmi_ 2>NUL
set gms_ 2>NUL
set gv1 2>NUL
set gv2 2>NUL

: Without 2>NULL , CMD will say 'Environment variable gmi not defined', when no env-var starts with gmi.
