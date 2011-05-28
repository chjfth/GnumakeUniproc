@echo off
set gmu_DIR_ROOT=%~dp0
set gmu_DIR_ROOT=%gmu_DIR_ROOT:~0,-1%
set gmu_DIR_ROOT=%gmu_DIR_ROOT:\=/%
:If full path of this .bat is D:\some\path\gmuenv.bat, resulting gmu_DIR_ROOT=D:/some/path
:More env-vars below are appended by GMU installer