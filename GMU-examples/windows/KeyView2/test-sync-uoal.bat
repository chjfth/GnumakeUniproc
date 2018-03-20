@REM Test using PI_sync_devoutput to sync gmi_SYDO_ud_SYNC_UserOutputAL_TO(i.e. gmp_up_USER_OUTPUT_AFTER_LINK)
@echo off
setlocal
set batdir=%~dp0
set batdir=%batdir:~0,-1%
set batdir_fs=%batdir:\=/%

@echo on
umake gmu_DO_SHOW_VERBOSE=2 gmp_u_list_PLUGIN_TO_LOAD_ENV_PRE="PI_sync_devoutput" gmi_SYDO_ud_SYNC_UserOutputAL_TO=%batdir_fs% gmi_SYDO_SHOW_COPY_CMD=1