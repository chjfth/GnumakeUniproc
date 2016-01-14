@set tmpbatdir=%~dp0
@set tmpbatdir=%tmpbatdir:~0,-1%

@SET NLSSVN=https://nlssvn/svnreps

set gv1=gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1
set gv2=gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1

@set tmpdirgmu=%tmpbatdir%\GMU-main\umake_cmd\wincmd
@PATH=%PATH%;%tmpdirgmu%
@echo GMU command PATH added: %tmpdirgmu% 

@call gmu-goody.bat

