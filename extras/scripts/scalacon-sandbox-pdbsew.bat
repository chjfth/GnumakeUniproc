@echo off
if "%1" == "" (
	echo Please assign a local svn sandbox directory as parameter. 
	echo If you use Scalacon 2016 style SDK, there should an "sdkin" sub-directory inside.
	exit /b 1
)

set dirsandbox=%1

@echo on
scalacon-ssindex-svn.py --dir-pdb=%dirsandbox% --dirs-source=%dirsandbox% --svn-use-export --loosy-reposie-table --pick-sstreams-dirs=sdkin --sdkin-doth-localroot=sdkin/include --dir-pdb-exclude-pattern=*cache*,sdkin
