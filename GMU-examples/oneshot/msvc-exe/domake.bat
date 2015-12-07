@echo off
setlocal

@echo off
set CURPATH=%CD%
set gmp_ud_list_CUSTOM_COMPILER_CFG=%CURPATH:\=/%
rem		Make current abspath / separated.

set gmp_COMPILER_ID=vcexe

umake %*
