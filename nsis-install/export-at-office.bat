@echo off
REM If I'm in nlscan office, just call this bat to export ALL files necessary
REM to pack a GnumakeUniproc Win32 release.
REM
REM 2010-01-12 Memo:
REM I have to manually build new make 3.81 and win-bash exe into MinGW-binary for a complete Windows version release.
@echo ON

if exist nsis-data rd /s /q nsis-data

call export-gmu.bat https://nlssvn/svnreps/makingsys/GnumakeUniproc
@if ERRORLEVEL 1 goto ErrSvnError

call export-gmu-bin.bat  https://nlssvn/BinaryRls/MinGW-binary
@if ERRORLEVEL 1 goto ErrSvnError

@where makensis > NUL
@if ERRORLEVEL 1 ( 
	echo.
	echo Export done, but makensis.exe not found in path. No exe is generated.
	exit /b 0
) else (
	makensis GMU-nsis.nsi
)

@if ERRORLEVEL 1 goto ErrSvnError

@echo.
@echo ==== SUCCESS ====
@goto END

:ErrSvnError
@echo SVN export fail!!!

:END