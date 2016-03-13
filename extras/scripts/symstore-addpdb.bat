@echo off
setlocal

call :CheckPath ret symstore.exe
if "%ret%" == "" (
  echo Error: symstore.exe is not in your PATH.
  exit /b 1
)


if "%4" == "" (
  echo symstore-addpdb.bat v1.0
  echo symstore-addpdb ^<pdb-local-dir^> ^<pdb-remote-dir^> ^<product-name^> ^<product-ver^> %5 %6 %7 %8 %9
  exit /b 1
)

set PdbLocalDir=%1
set PdbRemoteDir=%2
set ProductName=%3
set ProductVer=%4

@echo on
symstore add /r /f %PdbLocalDir%\*.pdb /s %PdbRemoteDir% /t %ProductName% /v %ProductVer% /c "Added on %DATE% %TIME%" %5 %6 %7 %8 %9


goto :eof


:CheckPath
set %~1=%~$PATH:2
exit /b

:eof
