setlocal
REM Don't call this bat directly, instead, call umake.bat, umakeD.bat etc.

set tmpbatdir=%~dp0%
set gmu_DIR_ROOT_bs=%tmpbatdir:\GMU-main\umake_cmd\wincmd\=%
set gmu_DIR_ROOT=%gmu_DIR_ROOT_bs:\=/%
:	gmu_DIR_ROOT will result in something like D:/GMU

REM PATH=%tmpbatdir%;%PATH% // This is unnecessary, because %tmpbatdir% must have been in the PATH, otherwise umake.bat cannot be reached.

call %gmu_DIR_ROOT_bs%\_gmuenv.bat


IF "%gmu_MAKE_EXE%" == "" (
      set gmu_MAKE_EXE=make
    )

REM Delete GnumakeUniproc start-up signature file
IF EXIST _MainPrjBuildStart.gmu.ckt DEL _MainPrjBuildStart.gmu.ckt
IF EXIST _MainPrjBuildStart.gmu.ckt GOTO ErrorDelGmuSig


IF "x%gmu_LOG_OUTPUT_FILENAME%x" == "xx" goto NoLogOutput

if "%gmu_LOG_APPEND%" == "1" goto LOG_READY
REM	-- we should not clear existing log when gmu_LOG_APPEND=1

REM Backup old log file by renaming
SET gmu_LOG_OUTPUT_FILENAME_bak=%gmu_LOG_OUTPUT_FILENAME%.bak

IF EXIST %gmu_LOG_OUTPUT_FILENAME_bak% DEL %gmu_LOG_OUTPUT_FILENAME_bak%
IF EXIST %gmu_LOG_OUTPUT_FILENAME_bak% goto ErrorDelLogBak

IF EXIST %gmu_LOG_OUTPUT_FILENAME% REN %gmu_LOG_OUTPUT_FILENAME% %gmu_LOG_OUTPUT_FILENAME_bak%
IF ERRORLEVEL 1 GOTO ErrorRename

:LOG_READY

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

%gmu_MAKE_EXE% --version > NUL 2>&1
if ERRORLEVEL 1 (
	echo ERROR: GNU make executable "%gmu_MAKE_EXE%" not found on this machine!
	goto END
)

REM Use special name for MD,MV,RM to avoid possible conflict of same-name EXE on user's existing env.
set MD_=mkdir_ -p
set RM_=rm_ -fr
set MV_=mv_
set CP_=cp_

if "%gmu_LOG_APPEND%" == "1" (
	%gmu_MAKE_EXE% %_F_MAKEFILE% %* 2>&1 | mtee /+ "%gmu_LOG_OUTPUT_FILENAME%"
) else (
	%gmu_MAKE_EXE% %_F_MAKEFILE% %* 2>&1 | mtee "%gmu_LOG_OUTPUT_FILENAME%"
)

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

REM Determine success/fail by comparing time stamp
REM Thanks to: http://stackoverflow.com/questions/1687014/how-do-i-compare-timestamps-of-files-in-a-dos-batch-script
REM I assume that umake's execution time is at least one second, and do not use the ~t compare skill, which report only "minute" time accurary.
SET FileStart=_MainPrjBuildStart.gmu.ckt
SET FileSuccess=_MainPrjBuildSuccess.gmu.ckt

if not exist %FileStart% if not exist %FileSuccess% (
	exit /b 0
REM Sigh, if the makefile does not use GMU, I don't know how to reliably check success state. 
)

FOR /F %%i IN ('dir /b /o:d %FileStart% %FileSuccess%') DO SET Newest=%%i
if %Newest% == %FileSuccess% (
	exit /b 0
) else (
	exit /b 4
)


