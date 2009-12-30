# Microsoft Developer Studio Project File - Name="Bash_builtins" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Static Library" 0x0104

CFG=Bash_builtins - Win32 Debug
!MESSAGE This is not a valid makefile. To build this project using NMAKE,
!MESSAGE use the Export Makefile command and run
!MESSAGE 
!MESSAGE NMAKE /f "Bash_builtins.mak".
!MESSAGE 
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "Bash_builtins.mak" CFG="Bash_builtins - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "Bash_builtins - Win32 Release" (based on "Win32 (x86) Static Library")
!MESSAGE "Bash_builtins - Win32 Debug" (based on "Win32 (x86) Static Library")
!MESSAGE 

# Begin Project
# PROP AllowPerConfigDependencies 0
# PROP Scc_ProjName ""
# PROP Scc_LocalPath ""
CPP=cl.exe
RSC=rc.exe

!IF  "$(CFG)" == "Bash_builtins - Win32 Release"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir "Release"
# PROP BASE Intermediate_Dir "Release"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 0
# PROP Output_Dir "Release"
# PROP Intermediate_Dir "Release"
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_MBCS" /D "_LIB" /YX /FD /c
# ADD CPP /nologo /MT /W3 /GX /O2 /I "..\..\v01\bash-1.14.2" /I "..\..\v01\bash-1.14.2\lib" /I "..\..\v01\dum_inc" /D "NDEBUG" /D "__NT_VC__" /D "WIN32" /D "_MBCS" /D "_LIB" /YX /FD /c
# ADD BASE RSC /l 0x804 /d "NDEBUG"
# ADD RSC /l 0x804 /d "NDEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LIB32=link.exe -lib
# ADD BASE LIB32 /nologo
# ADD LIB32 /nologo

!ELSEIF  "$(CFG)" == "Bash_builtins - Win32 Debug"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir "Debug"
# PROP BASE Intermediate_Dir "Debug"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 1
# PROP Output_Dir "Debug"
# PROP Intermediate_Dir "Debug"
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_MBCS" /D "_LIB" /YX /FD /GZ /c
# ADD CPP /nologo /MTd /W3 /Gm /GX /ZI /Od /I "..\..\v01\bash-1.14.2" /I "..\..\v01\bash-1.14.2\lib" /I "..\..\v01\dum_inc" /D "_DEBUG" /D "__NT_VC__" /D "WIN32" /D "_MBCS" /D "_LIB" /YX /FD /GZ /c
# ADD BASE RSC /l 0x804 /d "_DEBUG"
# ADD RSC /l 0x804 /d "_DEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LIB32=link.exe -lib
# ADD BASE LIB32 /nologo
# ADD LIB32 /nologo

!ENDIF 

# Begin Target

# Name "Bash_builtins - Win32 Release"
# Name "Bash_builtins - Win32 Debug"
# Begin Group "Source Files"

# PROP Default_Filter "cpp;c;cxx;rc;def;r;odl;idl;hpj;bat"
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\alias.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\bashgetopt.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\bind.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\break.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\builtin.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\builtins.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\cd.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\colon.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\command.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\common.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\declare.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\echo.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\enable.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\eval.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\exec.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\exit.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\fc.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\fg_bg.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\getopt.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\getopts.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\hash.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\help.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\history.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\inlib.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\jobs.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\kill.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\let.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\psize.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\read.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\return.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\set.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\setattr.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\shift.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\source.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\suspend.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\test.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\times.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\trap.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\type.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\ulimit.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\umask.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\wait.c"
# End Source File
# End Group
# Begin Group "Header Files"

# PROP Default_Filter "h;hpp;hxx;hm;inl"
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\bashgetopt.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\builtext.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\common.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\getopt.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\hashcom.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\builtins\pipesize.h"
# End Source File
# End Group
# End Target
# End Project
