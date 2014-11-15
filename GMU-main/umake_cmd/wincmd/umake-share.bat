REM Don't call this bat directly, instead, call umake.bat, umakeD.bat etc.

IF "%gmu_MAKE_EXE%" == "" (
      set gmu_MAKE_EXE=make
    )

REM Delete GnumakeUniproc start-up signiture file
IF EXIST _MainPrjBuildStart.gmu.ckt DEL _MainPrjBuildStart.gmu.ckt
IF EXIST _MainPrjBuildStart.gmu.ckt GOTO ErrorDelGmuSig

REM set GMU_PATH_PRE_SAVE=%PATH%
	rem For the old sh.exe, The PATH value will change weirdly in sh.exe

IF "x%gmu_LOG_OUTPUT_FILENAME%x" == "xx" goto NoLogOutput

REM Backup old log file by renaming
SET gmu_LOG_OUTPUT_FILENAME_bak=%gmu_LOG_OUTPUT_FILENAME%.bak

IF EXIST %gmu_LOG_OUTPUT_FILENAME_bak% DEL %gmu_LOG_OUTPUT_FILENAME_bak%
IF EXIST %gmu_LOG_OUTPUT_FILENAME_bak% goto ErrorDelLogBak

IF EXIST %gmu_LOG_OUTPUT_FILENAME% REN %gmu_LOG_OUTPUT_FILENAME% %gmu_LOG_OUTPUT_FILENAME_bak%
IF NOT %ERRORLEVEL% == 0 GOTO ErrorRename

REM A special processing since GnumakeUniproc v0.98. Prefer Makefile.umk as default makefile than Makefile.
REM If there exists Makefile.umk, I'll pass ``-f Makefile.umk`` to make executable, unless user explicitly assign ``-f xxx``.
REM * If user provides -f xxx in command parameter, I'll pass those parameter to make .
REM * If user does not provide -f xxx, I'll call make with all user's parameter as well as appending -f Makefile.umk as make's extra parameters.
if exist Makefile.umk (
	set _F_MAKEFILE=-f Makefile.umk
	:CHECK_PARAM_AGAIN
	if "%~1" == "" (
	  goto CHECK_PARAM_DONE
	) else (
	  if "%~1" == "-f" (
	    set _F_MAKEFILE=
	    goto CHECK_PARAM_DONE
	  )
	  rem echo @@@%1
	  shift
	)
)
goto CHECK_PARAM_AGAIN
:CHECK_PARAM_DONE

%gmu_MAKE_EXE% %_F_MAKEFILE% %* 2>&1 | tee "%gmu_LOG_OUTPUT_FILENAME%"
goto END

:NoLogOutput
%gmu_MAKE_EXE% %_F_MAKEFILE% %*
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
