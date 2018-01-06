@echo off
setlocal
REM Don't call this bat directly, instead, call umake.bat, umakeD.bat etc.

if "%gmu_LOG_OUTPUT_FILENAME%" == "" set gmu_LOG_OUTPUT_FILENAME=_gmulog.txt
set gmu_LOG_OUTPUT_FILENAME_bak=%gmu_LOG_OUTPUT_FILENAME%.bak

REM My elegant teebat solution, auto-log whole .bat output to tee when this .bat is the root bat. 
REM So,
REM * If you are the end-user calling this .bat, gmu_LOG_OUTPUT_FILENAME will be generated with the 
REM   same content on screen.
REM * If you are using another wrapper bat to run this bat, you should set TEEBAT_WRAPPER_EXISTED=1
REM   so that this .bat does not use tee. In other word, your wrapper bat use tee.

if "%TEEBAT_WRAPPER_EXISTED%" == "" (

	if exist %gmu_LOG_OUTPUT_FILENAME_bak% del %gmu_LOG_OUTPUT_FILENAME_bak%
	if exist %gmu_LOG_OUTPUT_FILENAME_bak% (
		echo Cannot delete old logfile: %gmu_LOG_OUTPUT_FILENAME_bak% 
		exit /b 1
	)

	if exist %gmu_LOG_OUTPUT_FILENAME% ren %gmu_LOG_OUTPUT_FILENAME% %gmu_LOG_OUTPUT_FILENAME_bak%
	if ERRORLEVEL 1 (
		echo Cannot rename old %gmu_LOG_OUTPUT_FILENAME% to %gmu_LOG_OUTPUT_FILENAME_bak%
		exit /b 1
	)
	
	REM Now call self with tee.
	set TEEBAT_WRAPPER_EXISTED=1
	call %0 %* 2>&1 | mtee %gmu_LOG_OUTPUT_FILENAME%
	REM By using pipe on the above CMD line, we cannot be sure of %0's exit code,
	REM because ERRORLEVEL may indicate %0's exit code or tee's exit code. So we just exit with 0.
	exit /b 0 
)



set thisbatdir_=%~dp0%
set thisbatdir=%thisbatdir_:~0,-1%
set gmu_DIR_ROOT_bs=%thisbatdir:\GMU-main\umake_cmd\wincmd=%
set gmu_DIR_ROOT=%gmu_DIR_ROOT_bs:\=/%
:	gmu_DIR_ROOT will result in something like D:/GMU

set PATH=%thisbatdir%;%PATH% 
REM -- This is wise! It serves a great purpose: 
REM    umake.bat's path(= %thisbatdir%) can be put at tail of your PATH env at usually time.
REM    However, as soon as umake.bat is launched, %thisbatdir% is elevated to head of PATH, 
REM    so GMU will always run its own-bundled executables(like sh.exe cat.exe sed.exe).

if "%gmu_DONT_USE_GOODIES%" == "" (
REM	We defaultly 
	call %thisbatdir\%gmu-goody.bat
)

call %gmu_DIR_ROOT_bs%\_gmuenv.bat


IF "%gmu_MAKE_EXE%" == "" set gmu_MAKE_EXE=gmu-make
REM -- We use the executable name gmu-make.exe explicitly so not to conflict with make.exe from various gcc cross toolchains.

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
	exit /b 1
)

REM Use special name for MD,MV,RM to avoid possible conflict of same-name EXE on user's existing env.
set MD_=mkdir_ -p
set RM_=rm_ -fr
set MV_=mv_
set CP_=cp_


REM Delete GnumakeUniproc start-up signature file
IF EXIST _MainPrjBuildStart.gmu.ckt DEL _MainPrjBuildStart.gmu.ckt
IF EXIST _MainPrjBuildStart.gmu.ckt (
	echo ERROR: Cannot delete GnumakeUniproc start-up signature file^(_MainPrjBuildStart.gmu.ckt^) in current dir. GnumakeUniproc will not work.
	exit /b 1
)

%gmu_MAKE_EXE% %_F_MAKEFILE% %*


