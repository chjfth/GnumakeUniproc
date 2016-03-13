@echo off
setlocal

call :CheckPath ret symstore.exe
if "%ret%" == "" (
  echo Error: symstore.exe is not in your PATH.
  exit /b 1
)


if "%3" == "" (
  echo scalacon-symstore-tmp.bat v1.1
  echo scalacon-symstore-tmp ^<pdb-local-dir^> ^<product-name^> ^<product-ver^> %4 %5 %6 %7 %8 %9
  exit /b 1
)

set tmpdir=tempdir

set PdbLocalDir=%1
set ProductName=%2
set ProductVer=%~3 (from user %USERNAME% at %COMPUTERNAME%)

ver > null 

@echo on

scalacon-ssindex-svn.py --dir-pdb=%PdbLocalDir% --dir-source=%PdbLocalDir% --datetime-co=now --dir-reposie-table=%gmu_DIR_ROOT%/nlscan --loosy-reposie-table --svn-use-export --svnhost-table=%gmu_DIR_ROOT%/nlscan/svnhosttable.txt --logfile=%tmpdir%\scalacon-ssindex.log

@if not %ERRORLEVEL% == 0 (
    exit /b 1
  )

scalacon-symstore.py --dir-scan=%PdbLocalDir% --dir-store=\\winshad0\devshare\tmpSymbols --product-name="%ProductName%" --product-ver="%ProductVer%" --pattern-include=*.pdb --pattern-exclude=*.lib.pdb/vc?0.pdb/vc??0.pdb --tmpdir=%tmpdir% 

@echo off
if %ERRORLEVEL% == 0 (
    echo Operation success!
    echo    Check which files are stored : %tmpdir%\ssinput.txt
    echo    Check symstore verbose output: %tmpdir%\symstore-logfile.log
  ) else (
    echo Ooups! You've got error.
    exit /b 1
  )

goto :eof


:CheckPath
set %~1=%~$PATH:2
exit /b

:eof
