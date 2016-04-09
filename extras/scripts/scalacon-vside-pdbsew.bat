@echo off
setlocal

set batdir=%~dp0
set batdir=%batdir:~0,-1%

if "%2" == "" (
	echo Missing parameters. 
	echo   %~n0 ^<vs-solutiondir^> ^<pdb-dir^> [pdb-name-pattern]
	echo Note:
	echo   Your ^<vs-solutiondir^> must be an svn sandbox for PDB-sewing to work.
	exit /b 1
)

set dir_vssln=%~1
set tail=%dir_vssln:~-1%
if "%tail%" == "\" set dir_vssln=%dir_vssln:~,-1%
REM
set dir_pdb=%~2
set tail=%dir_pdb:~-1%
if "%tail%" == "\" set dir_pdb=%dir_pdb:~,-1%
REM -- strip trailing backslash, OTHERWISE, it trips the double-quote, very insidious!
REM -- i.e. 
REM		--dir-pdb-include-pattern="D:\wx3-samples\Debug\" "abc" "def"
REM will all go into a single argv[]

if "%~3" == "" ( 
  set pdb_name_pattern_param=--pdb-include-pattern=
) else (
  set pdb_name_pattern_param=--pdb-include-pattern="%~3" 
)

for %%x in (svn.exe) do set svnexe_dir=%%~dp$PATH:x
if not defined svnexe_dir (
  echo Error: You do not have svn.exe in your PATH. PDB-sewing cannot be done.
  exit /b 1
)
REM Draw svn.exe, srctool.exe into PATH, and don't need other disturbing things in PATH.
PATH=%batdir%;%batdir%\pdbsew;%svnexe_dir%

set dirsandbox=%dir_vssln%
set final_pycmd=scalacon-ssindex-svn.py --dir-pdb="%dirsandbox%" --dirs-source="%dirsandbox%" --svn-use-export --loosy-reposie-table --pick-sstreams-dirs="%dirsandbox%\sdkin" --sdkin-doth-localroot="%dirsandbox%\sdkin\include" --dir-pdb-exclude-pattern=*cache*,sdkin --dir-pdb-include-pattern="%dir_pdb%" %pdb_name_pattern_param%

@echo on
echo %final_pycmd%
%final_pycmd%
