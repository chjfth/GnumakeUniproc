@echo off
@setlocal

REM Usage: 
REM Copy this file to the directory where your PDBs resides(can be their parent dir). 
REM Execute that copied sew-and-store.bat, and it will start source-sewing PDBs inside.
REM your .bat directory.
REM A symstore dir will be generated along-side your .bat and slso a compressed .7z .
REM That symstore dir conforms to Microsoft Symbol Server directory structure so you can
REM copy it to your symbol server without any change.
REM Tip: No problem to check-in this copy of sew-and-store.bat to your source server.
REM
REM If you want to store the symstored-PDBs to a customized dir, just make another 
REM copy of this bat and change DIR_MY_SYMBOL_STORE(below) to your own like.

REM	set DIR_MY_SYMBOL_STORE=k:\MySymbols
set PRODUCT_NAME=product

set batdir=%~dp0
set batdir=%batdir:~0,-1%

set dir_symstore_here=%batdir%\symstore

if "%DIR_MY_SYMBOL_STORE%" == "" (
	set zip_symstore=1
	set DIR_MY_SYMBOL_STORE=%dir_symstore_here%
	REM: Remove this dir to make a clean output so that it can be copied to our real symbol server
	echo Removing old in-place symstore directory %dir_symstore_here%
	rd /s /q %dir_symstore_here%
)

echo on
call scalacon-sandbox-pdbsew %batdir%\..
@echo off
if ERRORLEVEL 1 (
    exit /b 1
)

echo on
scalacon-symstore.py --dir-scan=%batdir% --dir-store=%DIR_MY_SYMBOL_STORE% --3tier-symstore --product-name=%PRODUCT_NAME% --pattern-exclude-dir=symstore
@echo off
if ERRORLEVEL 1 (
    exit /b 1
)

set path7z=%batdir%\symstore-%PRODUCT_NAME%.7z
if "%zip_symstore%" == "1" (
	del "%path7z%"
	
	pushd %DIR_MY_SYMBOL_STORE%
	7z a "%path7z%" *
	popd
)

echo.
echo === SUCCESS ===
