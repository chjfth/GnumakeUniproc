@set tmpbatdir=%~dp0
@set tmpbatdir=%tmpbatdir:~0,-1%

@SET NLSSVN=https://nlssvn.dev.nls/svnreps

set gv1=gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1
set gv2=gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1

@set tmpdirgmu=%tmpbatdir%\extras\scripts;%tmpbatdir%\GMU-main\umake_cmd\wincmd

@REM For the following if/else, we have to turn to enabledelayedexpansion's help.
@setlocal enabledelayedexpansion
@if "%1" == "front" (
	set __tmpPATH=!tmpdirgmu!;!PATH!
) else (
	set __tmpPATH=!PATH!;!tmpdirgmu!
)
@endlocal & PATH=%__tmpPATH%

doskey gmuex1=cd %tmpbatdir%\GMU-examples\common\walkdir\examples\walkdir_ex1

set gmu_INTERACTIVE_ERROR_RETRY=1

@call gmu-goody.bat

