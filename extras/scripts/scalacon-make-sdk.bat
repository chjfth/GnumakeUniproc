@echo off
setlocal

if "%DIR_NLS_BUILD_ENV%" == "" (
  echo Env-var DIR_NLS_BUILD_ENV not set, so I cannot find the compiler sets to use.
  exit /b 1
) else (
  call %DIR_NLS_BUILD_ENV%\gmp-cenv-all.bat
)

rem set CURDIR=%CD%
rem set CURDIR_fs=%CURDIR:\=/%
	rem Not used now.


REM Set releasing-datetime for this SDK (gmu_SC_CHECKOUT_DATETIME):
REM If gmu_SC_CHECKOUT_DATETIME have value, use it, otherwise, I think the best bet is
REM using current time. 
REM gmu_SC_CHECKOUT_DATETIME is used later in PDB-sewing. 
set datetimecmd=date_ +"%%Y-%%m-%%d %%H:%%M:%%S"
if "%gmu_SC_CHECKOUT_DATETIME%" == "" (
	REM Note: Place less CMD commands here, so to avoid delayed-expansion format like !foobar! .
	for /F "usebackq delims=" %%i IN (`%datetimecmd%`) DO set gmu_SC_CHECKOUT_DATETIME=%%i
)
if "%gmu_SC_CHECKOUT_DATETIME%" == "" (
	echo Cannot get current datetime! Perhaps you do not have GNUWin32 date_.exe . Install GMU to get one.
	exit /b 1
)
:echo gmu_SC_CHECKOUT_DATETIME=%gmu_SC_CHECKOUT_DATETIME% (debug)


REM CMD_GETSDKIN is optional, but most SDK should have it.
if not "%CMD_GETSDKIN%" == "" (
	%CMD_GETSDKIN%
	if ERRORLEVEL 1 (
		echo Error executing CMD_GETSDKIN.
		exit /b 1
	)
) 

@echo on
call umaketime %*

if ERRORLEVEL 1 exit /b 1

@cp_ _gmulog.txt %gmb_thisrepo%/%gmb_dirname_sdkout%
@cp_ gf/_building_list.gmu.txt  %gmb_thisrepo%/%gmb_dirname_sdkout%
REM -- In theory the filenames may not be _gmulog.txt or building_list.gmu.txt, but for simplicity, I just use the default.
