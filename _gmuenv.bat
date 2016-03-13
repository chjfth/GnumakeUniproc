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

SET gmu_ver=0.100

SET gmp_ud_list_CUSTOM_MKI=%gmp_ud_list_CUSTOM_MKI% %gmu_DIR_ROOT%/GMU-ext %gmu_DIR_ROOT%/nlscan/gmu-ext

SET gmp_ud_list_CUSTOM_COMPILER_CFG=%gmp_ud_list_CUSTOM_COMPILER_CFG% %gmu_DIR_ROOT%/nlscan/compiler-cfgs

SET gmp_DECO_PRJ_NAME=1

SET gmu_LOG_OUTPUT_FILENAME=_gmulog.txt

SET gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING=1

@if "%gmu_GCC_M_PREFIX_WEAK%" == "" (
	set gmu_GCC_M_PREFIX_WEAK=hdepend-
)
