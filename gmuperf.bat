@echo off
SETLOCAL EnableDelayedExpansion

::Check whether we are run from a directory with spaces in path. If so, stop it, since GMU does not support this.
set curdir=%CD%
if not "%curdir%" == "%curdir: =!%" (
  echo Sorry, GMU does not support run from a directory with spaces in it. Please change your current directory and try again.
  exit /b 1
  )

::Check whether GMU env has been set-up. If not, set it up.
set p_gmuenv_bat=%~dp0gmuenv.bat
if "%gmu_DIR_ROOT%" == "" (
  if exist %p_gmuenv_bat% (
    call %p_gmuenv_bat%
    ) else (
    echo Unexpected: %p_gmuenv_bat% does not exist. Fail to set GMU environment.
    exit /b 1
    )
  )

set p_PerfLog=%CD%\gmuperf.log

set pir_gfOutput=gf-gmuperf
set gmu_ud_OUTPUT_ROOT=%CD:\=/%/%pir_gfOutput%
	: Let GMU build output be inside current dir, so user can easily find it.
set gmu_ud_OUTPUT_ROOT=%gmu_ud_OUTPUT_ROOT://=/%
	: Otherwise, in case run from C:\ , gmu_ud_OUTPUT_ROOT will be C://gf-gmuperf
set BYPASS_GMUTEST_AUTO_CHECKOUT=1

::set dirMakeAll=%~dp0GMU-examples\common\walkdir\examples\walkdir_ex1\exe.mingw
set dirMakeAll=%~dp0GMU-examples\make-all\all-on-windows\all.mingw
set dirMakeAll=%dirMakeAll:\=/%

if "%1" == "" (
  set cycles=1
  ) else ( 
  set cycles=%1
  )
if "%cycles%" == "1" (
  set str_num_cycles=1 cycle
  ) else ( 
  set str_num_cycles=%cycles% cycles
  )

rm -fr %gmu_ud_OUTPUT_ROOT% :clear stale or old output content

set "startTime=%time%"

for /L %%i in (1,1,%cycles%) do (
	cmd /C "title Starting GMU test performance cycle %%i ..."
		:Use ``cmd /C'' so that the new title is reverted to original when this .bat quits.
	set gmu_u_SHOW_PROGRESS_CMD=cmd /C "title [gmuperf cycle %%i] GMU Progress: $(gmu_progress_info)"
	call make -C %dirMakeAll% gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1
		:Use make instead of umake, because I cannot get error code from umake.bat today.
	if not !ERRORLEVEL! == 0 (
	  echo.
	  echo ^<^<^< GMU make execution error, time used is not displayed. ^>^>^>
	  exit /b
	  )
	)

set "stopTime=%time%"

call :timeDiff diff startTime stopTime
set /A _sec_=%diff% / 1000
set /A _msec_=%diff% %% 1000

echo.
echo ^<^<^< %str_num_cycles% done, total seconds used: %_sec_%.%_msec_% ^>^>^>

:Write(append) result to log file
for /F "usebackq delims=" %%i IN (`ver`) DO set str_winver=%%i
for /F "usebackq tokens=1,2,3" %%i in (`gmucountchar %pir_gfOutput%\_gmu_tmp\_CountCompile.gmu.cnt += R r`) do set str_prjcount=Projects:%%i,Containers:%%j+%%k
echo [%DATE% %TIME:~0,-3%] %str_winver% GMU v%gmu_ver% %str_prjcount%, %str_num_cycles%, %_sec_%.%_msec_% seconds. >>%p_PerfLog%

goto :eof


:##############################################################################
:Thanks to jeb from http://stackoverflow.com/questions/4487100/how-can-i-use-a-windows-batch-file-to-measure-the-performance-of-console-applicat for providing the timeDiff function.
:But note: this function can not cope well across 00:00 boundary currently.

:timeDiff
setlocal
call :timeToMS time1 "%~2"
call :timeToMS time2 "%~3"
set /a diff=time2-time1
(
  ENDLOCAL
  set "%~1=%diff%"
  goto :eof
)

:timeToMS
::### WARNING, enclose the time in " ", because it can contain comma seperators
SETLOCAL EnableDelayedExpansion
FOR /F "tokens=1,2,3,4 delims=:,.^ " %%a IN ("!%~2!") DO (
  set /a "ms=(((30%%a%%100)*60+7%%b)*60+3%%c-42300)*1000+(1%%d0 %% 1000)"
)
(
  ENDLOCAL
  set %~1=%ms%
  goto :eof
)

