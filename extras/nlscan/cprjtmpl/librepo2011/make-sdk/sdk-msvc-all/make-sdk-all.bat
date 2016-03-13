@echo off
setlocal
set CURPATH=%CD:\=/%

:set gmi_SYDO_SHOW_COPY_CMD=1

IF "%gmb_syncto%" == "" (
	echo SET gmb_syncto=%CURPATH%/nlssdk
         SET gmb_syncto=%CURPATH%/nlssdk
  )

@echo on
umaketime gmb_compiler_ids="" gmb_msvc_vers="" gmb_wince_vers="" %*
