@REM Don't call this batch file directly; it should be called by a wrapper bat, umake-share.bat etc.

@if "%gmu_DIR_ROOT%" == "" (
	echo ERROR from _gmuenv.bat: Env-var gmu_DIR_ROOT not defined yet.
	exit /b 1
)
@if "%gmu_DIR_ROOT_bs%" == "" (
	echo ERROR from _gmuenv.bat: Env-var gmu_DIR_ROOT_bs not defined yet.
	exit /b 1
)


SET gmu_DIR_GNUMAKEUNIPROC=%gmu_DIR_ROOT%/GMU-main/GnumakeUniproc

SET gmu_ver=0.99

SET gmp_ud_list_CUSTOM_MKI=%gmp_ud_list_CUSTOM_MKI% %gmu_DIR_ROOT%/GMU-ext %gmu_DIR_ROOT%/nlscan/gmu-ext

SET gmp_ud_list_CUSTOM_COMPILER_CFG=%gmu_DIR_ROOT%/nlscan/compiler-cfgs

SET gmp_DECO_PRJ_NAME=1

SET gmu_LOG_OUTPUT_FILENAME=_gmulog.txt

SET gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING=1

set gmuex1=%gmu_DIR_ROOT%/GMU-examples/common/walkdir/make-all
set gv1=gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1
set gv2=gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1

@REM Normally, gmu_BIN_PATH_TAIL is not defined
@if "%gmu_BIN_PATH_TAIL%" == "" (
	PATH=%gmu_DIR_ROOT_bs%\MinGW2\bin;%PATH%
) else (
	PATH=%PATH%;%gmu_DIR_ROOT_bs%\MinGW2\bin
)

SET NLSSVN=https://nlssvn/svnreps

