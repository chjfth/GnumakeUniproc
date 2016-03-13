@echo off
if "x%~1x" == "xx" goto ErrParamMissing
	REM The ~ is to deal with space chars in %1, e.g. %1="C:\VS 2005"

set _gmp_tmp_device=%2
	rem %2 is optional

set gmu_u_GCC_M_OPTIONS=-D_M_ARM
	REM VS2005 ARM compiler defines _M_ARM internally, so we pass it to 'gcc -M' as well.

set VSInstallDir=%~1
set VCInstallDir=%VSInstallDir%\VC
set VCCeDir=%VCInstallDir%\ce

@echo on
set INCLUDE=%VCInstallDir%\ce\include;%VCInstallDir%\ce\atlmfc\include;
	@rem Only these two dirs are invariant whatever the target device is.

@IF "%_gmp_tmp_device%" == "pocketpc2003" (
	  echo Added pocketpc2003 INCLUDE and LIB path.
      set INCLUDE=%VSInstallDir%\SmartDevices\SDK\PocketPC2003\include;%INCLUDE%;
      set     LIB=%VSInstallDir%\SmartDevices\SDK\PocketPC2003\lib\ARMV4;%VCCeDir%\atlmfc\lib\ARMV4;%VCCeDir%\lib\ARMV4;
    ) ELSE IF "%vv%" == "smartphone2003" (
	  echo Added smartphone2003 INCLUDE and LIB path.
      set INCLUDE=%VSInstallDir%\SmartDevices\SDK\SmartPhone2003\include;%INCLUDE%;
      set     LIB=%VSInstallDir%\SmartDevices\SDK\SmartPhone2003\lib\ARMV4;%VCCeDir%\atlmfc\lib\ARMV4;%VCCeDir%\lib\ARMV4;
    ) ELSE (
      echo Info: Neither pocketpc2003 or smartphone2003 is given as second param. Device specific INCLUDE and LIB path not set yet.
    )

PATH=%VCCeDir%\bin\x86_arm;%VSInstallDir%\Common7\IDE;%VCInstallDir%\bin;%PATH%

@echo off
goto END

:ErrParamMissing
echo You must assign a param as VSInstallDir. 
echo Example: 
echo   %~n1 E:\VS8

:END
