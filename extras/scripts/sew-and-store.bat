@echo off
@setlocal

REM Usage: 
REM Copy this file to the SVN sandbox directory where you have compiled your EXE/DLL/SYS
REM binary with PDBs generated (can be their parent dir). 
REM Execute this copied sew-and-store.bat in your sandbox, and it will start source-sewing
REM PDBs inside your sandbox directory.
REM Note: You should copy this bat because it searchs PDBs from its containing directory.
REM A symstore dir will be generated along-side your .bat and also a compressed .7z .
REM That symstore dir conforms to Microsoft Symbol Server directory structure so you can
REM copy it to your symbol server without any change.
REM Tip: No problem to check-in this copy of sew-and-store.bat to your SVN server.
REM
REM If you want to also store(merge) the symstored-PDBs to a customized dir, 
REM set DIR_MY_SYMBOL_STORE(from env-var) to your own like.

REM	set DIR_MY_SYMBOL_STORE=k:\MySymbols
set PRODUCT_NAME=product

set batdir=%~dp0
set batdir=%batdir:~0,-1%

set dir_symstore_here=%batdir%\symstore

REM: Remove this dir to make a clean output so that it can be copied to our real symbol server
echo Removing old in-place symstore directory %dir_symstore_here%
rd /s /q %dir_symstore_here%


echo on
call scalacon-sandbox-pdbsew %batdir%
@echo off
if ERRORLEVEL 1 (
    exit /b 1
)
echo.

echo on
scalacon-symstore.py --dir-scan=%batdir% --dir-store=%dir_symstore_here% --3tier-symstore --product-name=%PRODUCT_NAME% --pattern-exclude-dir=symstore/.sdkbin-cache/sdkin*/sdkout*
@echo off
if ERRORLEVEL 1 (
    exit /b 1
)
echo.

if "%DIR_MY_SYMBOL_STORE%" == "" goto DO_ZIP

echo Will merge symbol store %dir_symstore_here% -^> %DIR_MY_SYMBOL_STORE%
echo on
symstore add /r /f %dir_symstore_here% /s %DIR_MY_SYMBOL_STORE% /t %PRODUCT_NAME%
@echo off
if ERRORLEVEL 1 (
	exit /b 1
)


:DO_ZIP
set path7z=%batdir%\symstore-%PRODUCT_NAME%.7z
if exist "%path7z%" del "%path7z%"

pushd %dir_symstore_here%
echo on
7z a "%path7z%" *
@echo off
popd

echo.
echo === SUCCESS ===
