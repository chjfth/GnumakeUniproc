@echo off
setlocal
REM This .bat file exports binary files for GnumakeUniproc NSIS packing.
REM These files(tens of mega-bytes) are not stored on sf.net, but on my nlssvn SVN server.
rem		https://nlssvn/BinaryRls/MinGW-binary
REM Tested with svn 1.4.2 (r22196)

if "x%1x" == "xx" goto ErrParamMissing

set SvnUrlPrefix=%1

set BranchToGet=trunk

if NOT "x%2x" == "xx" set BranchToGet=%2

set OutputDir=nsis-data

@echo on
svn export --force %SvnUrlPrefix%/%BranchToGet%/bin-gmu  %OutputDir%/bin-gmu
@if ERRORLEVEL 1 goto ErrSvnError
svn export --force %SvnUrlPrefix%/%BranchToGet%/bin-gmu-addons  %OutputDir%/bin-gmu-addons
@if ERRORLEVEL 1 goto ErrSvnError
svn export --force %SvnUrlPrefix%/%BranchToGet%/MinGW2   %OutputDir%/MinGW2
@if ERRORLEVEL 1 goto ErrSvnError
@echo off

@echo The binary files for NSIS to pack have been retrieved.
goto END

:ErrSvnError
@echo Unexpected! SVN export failed.
@goto END

:ErrParamMissing
@echo You must assign a param as the SVN Url prefix for SVN repository, and optionally a second param for branch to export(default to trunk).

:END
