@echo off
setlocal
call %DIR_NLS_BUILD_ENV%\gmp-cenv-all.bat

set CURDIR=%CD%
set CURDIR_fs=%CURDIR:\=/%

:set gmi_SYDO_SHOW_COPY_CMD=1

REM Set default sdkout directory (gmb_syncto):
REM We must use / (instead of \) even on Windows, otherwise it fails PI_sync_devoutput.
IF "%gmb_syncto%" == "" (
	echo SET gmb_syncto=%CURDIR_fs%/sdkout
         SET gmb_syncto=%CURDIR_fs%/sdkout
  )

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
umaketime %*
@REM ENV may have: gmb_compiler_ids="..." gmb_msvc_vers="..." gmb_wince_vers="..." 
