@echo off
REM !special: For convenience, I export NLSCAN related files and pack them into GMU.
rem	https://nlssvn/svnreps/makingsys
if "x%1x" == "xx" goto ErrParamMissing

set SvnUrlPrefix=%1

set BranchToGet=trunk

if NOT "x%2x" == "xx" set BranchToGet=%2

set OutputDir=nsis-data

@echo on
svn export --force %SvnUrlPrefix%/GMU-addons/%BranchToGet%/nlscan  %OutputDir%/GMU/nlscan
@if ERRORLEVEL 1 goto ErrSvnError

svn export --force %SvnUrlPrefix%/GMU-addons/%BranchToGet%/scripts  %OutputDir%/bin-gmu-addons
@if ERRORLEVEL 1 goto ErrSvnError

@REM Export helper ruby programs:
svn export --force %SvnUrlPrefix%/GmuDemoPack/%BranchToGet%  %OutputDir%/bin-gmu-addons
@if ERRORLEVEL 1 goto ErrSvnError

@echo NLSCAN related files have been retrieved.
@goto END

:ErrSvnError
@echo Unexpected! SVN export failed.
@goto END

:ErrParamMissing
@echo You must assign a param as the SVN Url prefix for SVN repository, and optionally a second param for branch to export(default to trunk).

:END
