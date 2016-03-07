@echo off
setlocal
set gmp_bc_DEBUG=1
set gmp_bc_UNICODE=1

call %~dp0umake-share.bat %*
