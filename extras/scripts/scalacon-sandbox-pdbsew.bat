@echo off
setlocal

REM This bat is called by sew-and-store.bat .

if "%1" == "" (
	echo Please assign a local svn sandbox directory as parameter. 
	echo If you use Scalacon 2016 style SDK, and you have "D:\myprj\sdkin", you should assign "D:\myprj" .
	exit /b 1
)

set dirsandbox=%1
REM Now strip its trailing backslash, so that --sdkin-doth-localroot does not get double slashes.
set tail=%dirsandbox:~-1%
if "%tail%" == "\" ( set dirsandbox=%dirsandbox:~,-1% )


shift

@echo on
scalacon-ssindex-svn.py --dir-pdb=%dirsandbox% --dirs-source=%dirsandbox% --svn-use-export --loosy-reposie-table --pick-sstreams-dirs=%dirsandbox%\sdkin --sdkin-doth-localroot=%dirsandbox%\sdkin\include --dir-pdb-exclude-pattern=*cache*,sdkin %1 %2 %3 %4 %5 %6 %7 %8 %9
