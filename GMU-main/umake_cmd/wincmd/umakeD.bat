@echo off
setlocal
set gmp_bc_DEBUG=1

call %~dp0umake-share.bat %*
