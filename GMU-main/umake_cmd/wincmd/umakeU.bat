@echo off
REM 'dir > null' resets the internal %ERRORLEVEL% to 0. We must do this because some internal cmd like "set" does not reset "ERRORLEVEL".
dir > nul
REM Delete GnumakeUniproc start-up signiture file
IF EXIST _MainPrjBuildStart.gmu.ckt DEL _MainPrjBuildStart.gmu.ckt
IF EXIST _MainPrjBuildStart.gmu.ckt GOTO ErrorDelGmuSig

set GMU_PATH_PRE_SAVE=%PATH%
	rem For the old sh.exe, The PATH value will change weirdly in sh.exe

IF "x%gmu_LOG_OUTPUT_FILENAME%x" == "xx" goto NoLogOutput

REM Backup old log file by renaming
SET gmu_LOG_OUTPUT_FILENAME_bak=%gmu_LOG_OUTPUT_FILENAME%.bak

IF EXIST %gmu_LOG_OUTPUT_FILENAME_bak% DEL %gmu_LOG_OUTPUT_FILENAME_bak%
IF EXIST %gmu_LOG_OUTPUT_FILENAME_bak% goto ErrorDelLogBak

IF EXIST %gmu_LOG_OUTPUT_FILENAME% REN %gmu_LOG_OUTPUT_FILENAME% %gmu_LOG_OUTPUT_FILENAME_bak%
IF NOT %ERRORLEVEL% == 0 GOTO ErrorRename

make%gmu_MAKEEXESUFFIX% gmp_bc_UNICODE=1 %* 2>&1 | tee "%gmu_LOG_OUTPUT_FILENAME%"
goto END

:NoLogOutput
make%gmu_MAKEEXESUFFIX% gmp_bc_UNICODE=1 %*
GOTO END

:ErrorDelGmuSig
echo Error from %0: Cannot delete GnumakeUniproc start-up signature file(_MainPrjBuildStart.gmu.ckt) in current dir. GnumakeUniproc will not work.
goto END

:ErrorDelLogBak
echo Error from %0: Cannot delete backup log-file(%gmu_LOG_OUTPUT_FILENAME_bak%) .
goto END

:ErrorRename
echo Error from %0: Cannot Rename %gmu_LOG_OUTPUT_FILENAME% to %gmu_LOG_OUTPUT_FILENAME_bak% .
goto END

:END