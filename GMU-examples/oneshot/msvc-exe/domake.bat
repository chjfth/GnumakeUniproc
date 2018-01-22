@echo off
REM Use setlocal so that 'myvc' does not affect user's environment
setlocal

REM Set gmp_COMPILER_ID to anything you like, it just cannot be empty as required by GMU.
set gmp_COMPILER_ID=myvc


REM set CURPATH=%CD%
REM gmp_ud_list_CUSTOM_COMPILER_CFG=%CURPATH:\=/%
rem		Make current abspath / separated. 
rem		You may wish to define gmp_ud_list_CUSTOM_COMPILER_CFG if you have more than one project
rem		sharing the same set of compiler_config.mki .
rem		Example: If 
rem			gmp_ud_list_CUSTOM_COMPILER_CFG=D:/myprj
rem		you should prepare accordingly:
rem			D:/myprj/myvc/compiler_config.mki

umake %*
