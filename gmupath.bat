@set tmpbatdir=%~dp0
@set tmpbatdir=%tmpbatdir:~0,-1%

@SET NLSSVN=https://nlssvn/svnreps

@set _gmuex1=%tmpbatdir%\GMU-examples\common\walkdir\make-all

set gv1=gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1
set gv2=gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1

@set tmpdir=%tmpbatdir%\GMU-main\umake_cmd\wincmd
@REM -- No need to add %tmpbatdir%\MinGW2\bin here, it will be added in _gmuenv.bat
@PATH=%tmpdir%;%PATH%

@call gmu-goody.bat

@echo GMU command PATH added: %tmpdir% 
