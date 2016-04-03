@echo off
setlocal

set SCALACON_LOGFILE=_scalacon.gmulog.txt
set SCALACON_LOGFILE_bak=%SCALACON_LOGFILE%.bak

REM My elegant teebat solution, auto-log whole .bat output to tee(mtee) when this .bat is the root bat. 
REM So,
REM * If you are the end-user calling this .bat, SCALACON_LOGFILE will be generated with the 
REM   same content on screen.
REM * If you are using another wrapper bat to run this bat, you should set SCALACON_WRAPPER_EXISTED=1
REM   so that this .bat does not use tee. In other word, your wrapper bat use tee.

if "%SCALACON_WRAPPER_EXISTED%" == "" (

	if exist %SCALACON_LOGFILE_bak% del %SCALACON_LOGFILE_bak%
	if exist %SCALACON_LOGFILE_bak% (
		echo Cannot delete old logfile: %SCALACON_LOGFILE_bak% 
		exit /b 1
	)

	if exist %SCALACON_LOGFILE% ren %SCALACON_LOGFILE% %SCALACON_LOGFILE_bak%
	if ERRORLEVEL 1 (
		echo Cannot rename old %SCALACON_LOGFILE% to %SCALACON_LOGFILE_bak%
		exit /b 1
	)

	set SCALACON_WRAPPER_EXISTED=1

	call %0 %* 2>&1 | mtee %SCALACON_LOGFILE%
	REM By using pipe on the above CMD line, we cannot be sure of %0's exit code,
	REM because ERRORLEVEL may indicate %0's exit code or tee's exit code. So we just exit with 0.
	exit /b 0 
)



if "%DIR_NLS_BUILD_ENV%" == "" (
  echo Env-var DIR_NLS_BUILD_ENV not set, so I cannot find the compiler sets to use.
  exit /b 1
) else (
  call %DIR_NLS_BUILD_ENV%\gmp-cenv-all.bat
  if errorlevel 1 exit /b 1
)


rem set CURDIR=%CD%
rem set CURDIR_fs=%CURDIR:\=/%
	rem Not used now.

REM CMD_GETSDKIN is optional, but most SDK should have it.
if not "%CMD_GETSDKIN%" == "" (
	%CMD_GETSDKIN%
	if ERRORLEVEL 1 (
		echo Error executing CMD_GETSDKIN.
		exit /b 1
	)
) 

@echo on
set gmu_WRAPPER_EXISTED=1
REM -- this is important to get correct umaketime exit code.

call umaketime %*

@if ERRORLEVEL 1 exit /b 1

@echo off

cp_ %SCALACON_LOGFILE% %gmb_thisrepo%/%gmb_dirname_sdkout%
if ERRORLEVEL 1 (
	echo Error executing: cp_ %SCALACON_LOGFILE% %gmb_thisrepo%/%gmb_dirname_sdkout%
	exit /b 1
)

@if "%gmu_ud_OUTPUT_ROOT%" == "" ( 
	set GF_DIR=gf
) else (
	set GF_DIR=%gmu_ud_OUTPUT_ROOT%
)

cp_ %GF_DIR%/_building_list.gmu.txt  %gmb_thisrepo%/%gmb_dirname_sdkout%
@REM -- In theory the filenames may not be building_list.gmu.txt, but for simplicity, I just use the default.
if ERRORLEVEL 1 (
	echo Error executing: cp_ %GF_DIR%/_building_list.gmu.txt  %gmb_thisrepo%/%gmb_dirname_sdkout%
	exit /b 1
)

set file7z=%gmb_sdkname%-%DATE%.7z
set cmd7z=7z a %gmb_thisrepo%/%file7z% %gmb_thisrepo%/%gmb_dirname_sdkout% %gmb_thisrepo%/websymbols
%cmd7z% 2>&1 > 7z.log
if ERRORLEVEL 1 (
	echo Error executing: %cmd7z%
)

echo.
echo Generated SDK package %file7z% .

echo.
echo ////////// SCALACON MAKE-SDK SUCCESS //////////
echo.
