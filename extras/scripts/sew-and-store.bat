@echo off
@setlocal

REM Usage: 
REM This bat searches your base directory(basedir) for PDBs and apply PDB-sewing to them,
REM and, stores the sewed PDBs to a clean $basedir\symstore (compressed to .7z as well). 
REM Then, you can copy the files in symstore directory to your real symbol-server.
REM
REM If you run this bat with no parameter, basedir is your current working directory.
REM If you explicitly assign a parameter, it will be become basedir.
REM
REM Note: Your basedir should be an SVN sandbox for PDB-sewing to work..
REM
REM Additionally, you can set env-var 
REM		DIR_MY_SYMBOL_STORE=D:\MySymbols
REM
REM so to have the generated symstore content copied(merge) to D:\MySymbols .

set PRODUCT_NAME=any

if "%1" == "" (
	set basedir=%CD%
) else (
	set basedir=%1
)

set dir_symstore_here=%basedir%\symstore

REM: Remove this dir to make a clean output so that it can be copied to our real symbol server
echo Removing old in-place symstore directory %dir_symstore_here%
rd /s /q %dir_symstore_here%


echo on
call scalacon-sandbox-pdbsew %basedir%
@echo off
if ERRORLEVEL 1 (
	echo !!! Error occurred !!!
    exit /b 1
)
echo.

echo on
scalacon-symstore.py --dir-scan=%basedir% --dir-store=%dir_symstore_here% --3tier-symstore --product-name=%PRODUCT_NAME% --pattern-exclude-dir=symstore/.sdkbin-cache/sdkin*/sdkout*
@echo off
if ERRORLEVEL 1 (
	echo !!! Error occurred !!!
    exit /b 1
)
echo.

if "%DIR_MY_SYMBOL_STORE%" == "" (
	echo Env-var DIR_MY_SYMBOL_STORE is empty, will not merge symstore.
	goto DO_ZIP
)

echo Will merge symbol store %dir_symstore_here% -^> %DIR_MY_SYMBOL_STORE%

for %%x in (scalacon-symstore.py) do set tmp_pypath=%%~$PATH:x
set dir_gmucmd=%tmp_pypath:\scalacon-symstore.py=%

echo on
%dir_gmucmd%\pdbsew\symstore add /r /f %dir_symstore_here% /s %DIR_MY_SYMBOL_STORE% /t %PRODUCT_NAME%
@echo off
if ERRORLEVEL 1 (
	echo !!! Error occurred !!!
	exit /b 1
)


:DO_ZIP
for /F "usebackq delims=" %%i IN (`date_ +%%Y%%m%%d_%%H%%M%%S`) DO set dtstr=%%i
set path7z=%basedir%\symstore-%dtstr%.7z
if exist "%path7z%" del "%path7z%"

pushd %dir_symstore_here%
echo on
7z a "%path7z%" *
@echo off
popd

echo.
echo === SUCCESS ===
