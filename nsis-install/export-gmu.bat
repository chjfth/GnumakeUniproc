@echo off
REM This .bat file exports data from GnumakeUniproc's SVN repository for NSIS packing.
REM [2007-03-02] Currently, the prefix from sf.net is
REM   https://gnumakeuniproc.svn.sourceforge.net/svnroot/gnumakeuniproc
rem (chj internal use): 
rem		https://nlssvn/svnreps/makingsys/GnumakeUniproc
REM Tested with svn 1.4.2 (r22196)

if "x%1x" == "xx" goto ErrParamMissing

set SvnUrlPrefix=%1

set BranchToGet=trunk

if NOT "x%2x" == "xx" set BranchToGet=%2

set OutputDir=nsis-data

@echo on
svn export --force %SvnUrlPrefix%/%BranchToGet%     %OutputDir%/GMU
@if ERRORLEVEL 1 goto ErrSvnError
@echo off

@echo Files for NSIS to pack have been retrieved.
goto END

:ErrSvnError
@echo Unexpected! SVN export failed.
@goto END

:ErrParamMissing
@echo You must assign a param as the SVN Url prefix for GnumakeUniproc SVN repository, and optionally a second param for branch to export(default to trunk).

:END
