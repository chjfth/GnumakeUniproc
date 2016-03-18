@REM This makes the cmd.exe window title shows GMU build progress.
SET gmu_u_SHOW_PROGRESS_CMD=CMD /C "title GMU Progress: $(gmu_progress_info)"

SET gmu_SHCMD_ALERT_ERROR=CMD /C "title GMU Got Error @ $2"
@REM		$1: the root-makefile fullpath ; $2: $1: sub-makefile fullpath causing the error
