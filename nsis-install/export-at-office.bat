REM If I'm in nlscan office, just call this bat to export ALL files necessary
REM to pack a GnumakeUniproc Win32 release.
REM
REM 2010-01-12 Memo:
REM I have to manually build new make 3.81 and win-bash exe into MinGW-binary for a complete Windows version release.

rd /s /q nsis-data

call export-gmu.bat https://nlssvn/svnreps/makingsys/GnumakeUniproc
@if ERRORLEVEL 1 goto ErrSvnError

call export-gmu-bin.bat  https://nlssvn/BinaryRls/MinGW-binary
@if ERRORLEVEL 1 goto ErrSvnError

@echo All exports success.
@goto END

:ErrSvnError
@echo SVN export fail!!!

:END