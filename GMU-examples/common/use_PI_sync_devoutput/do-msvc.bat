@REM This file is run as Microsoft Windows console command(Win2000 or above).
pushd ..\walkdir\libsrc\makelib\lib.msvc
call umake gmu_DO_SHOW_VERBOSE=2 gmp_u_list_PLUGIN_TO_LOAD=PI_sync_devoutput gmi_SYDO_ud_SYNC_HEADER_TO=%gmu_DIR_ROOT%/mysdk/include gmi_SYDO_ud_SYNC_LIB_TO=%gmu_DIR_ROOT%/mysdk/lib %*
popd
