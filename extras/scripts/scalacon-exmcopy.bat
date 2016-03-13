@echo off

if "%2" == "" (
  echo Error: Parameter missing.
  echo Usage: %~n0 ^<from-dir^> ^<to-dirname^>
  echo Note:
  echo     ^<from-dir^> can be a directory with optional path prefix.
  echo     ^<to-dirname^> must be a new directory name, without path prefix.
  exit /b 1
)

if not "%2" == "%~n2" (
  echo Error: Second parameter must not have path prefix, only a name is allowed.
  exit /b 1
)

@echo on
scalacon-deep-rename.py --copy --topdir=%1 --oldname=%~n1 --newname=%2 --update-uuid-by-keys=ProjectGUID
