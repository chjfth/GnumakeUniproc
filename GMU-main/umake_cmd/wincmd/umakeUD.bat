@echo off
REM 'dir > null' resets the internal %ERRORLEVEL% to 0. We must do this because some internal cmd like "ECHO", "SET" or "IF" does not reset "ERRORLEVEL", and if so, a non-zero %ERRRORLEVEL% from CMD environment will strike ``IF NOT %ERRORLEVEL% == 0 GOTO ErrorRename'' thus cause failure. [2009-05-14] Today, use setlocal instead of ``dir>null''to kill two birds with one stone.
setlocal
set gmp_bc_DEBUG=1
set gmp_bc_UNICODE=1

call %~dp0umake-share.bat
