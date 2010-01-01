# Microsoft Developer Studio Project File - Name="Bash" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Console Application" 0x0103

CFG=Bash - Win32 Debug
!MESSAGE This is not a valid makefile. To build this project using NMAKE,
!MESSAGE use the Export Makefile command and run
!MESSAGE 
!MESSAGE NMAKE /f "Bash.mak".
!MESSAGE 
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "Bash.mak" CFG="Bash - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "Bash - Win32 Release" (based on "Win32 (x86) Console Application")
!MESSAGE "Bash - Win32 Debug" (based on "Win32 (x86) Console Application")
!MESSAGE 

# Begin Project
# PROP AllowPerConfigDependencies 0
# PROP Scc_ProjName ""
# PROP Scc_LocalPath ""
CPP=cl.exe
RSC=rc.exe

!IF  "$(CFG)" == "Bash - Win32 Release"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir "Release"
# PROP BASE Intermediate_Dir "Release"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 0
# PROP Output_Dir "Release"
# PROP Intermediate_Dir "Release"
# PROP Ignore_Export_Lib 0
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /c
# ADD CPP /nologo /MT /W3 /GX /O2 /I "..\..\v01\bash-1.14.2\win32-subproc" /I "..\..\v01\bash-1.14.2" /I "..\..\v01\bash-1.14.2\lib" /I "..\..\v01\dum_inc" /D "NDEBUG" /D Program=bash /D "__NT_VC__" /D "INITIALIZE_SIGLIST" /D "HAVE_VFPRINTF" /D "HAVE_UNISTD_H" /D "HAVE_STDLIB_H" /D "HAVE_LIMITS_H" /D "HAVE_RESOURCE" /D "HAVE_SYS_PARAM" /D "HAVE_DIRENT_H" /D "VOID_SIGHANDLER" /D "BROKEN_SIGSUSPEND" /D "HAVE_GETHOSTNAME" /D "MKFIFO_MISSING" /D "NO_DEV_TTY_JOB_CONTROL" /D "NO_SBRK_DECL" /D "PGRP_PIPE" /D "TERMIOS_MISSING" /D "HAVE_DUP2" /D "HAVE_STRERROR" /D "HAVE_DIRENT" /D "HAVE_STRING_H" /D "HAVE_VARARGS_H" /D "HAVE_STRCHR" /D "SHELL" /D "HAVE_ALLOCA" /D "HAVE_ALLOCA_H" /D "WIN32" /D "_CONSOLE" /D "_MBCS" /YX /FD /c
# ADD BASE RSC /l 0x804 /d "NDEBUG"
# ADD RSC /l 0x804 /d "NDEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:console /machine:I386
# ADD LINK32 kernel32.lib user32.lib Advapi32.lib /nologo /subsystem:console /machine:I386

!ELSEIF  "$(CFG)" == "Bash - Win32 Debug"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir "Debug"
# PROP BASE Intermediate_Dir "Debug"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 1
# PROP Output_Dir "Debug"
# PROP Intermediate_Dir "Debug"
# PROP Ignore_Export_Lib 0
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /GZ /c
# ADD CPP /nologo /MTd /W3 /Gm /GX /ZI /Od /I "..\..\v01\bash-1.14.2\win32-subproc" /I "..\..\v01\bash-1.14.2" /I "..\..\v01\bash-1.14.2\lib" /I "..\..\v01\dum_inc" /D "_DEBUG" /D Program=bash /D "__NT_VC__" /D "INITIALIZE_SIGLIST" /D "HAVE_VFPRINTF" /D "HAVE_UNISTD_H" /D "HAVE_STDLIB_H" /D "HAVE_LIMITS_H" /D "HAVE_RESOURCE" /D "HAVE_SYS_PARAM" /D "HAVE_DIRENT_H" /D "VOID_SIGHANDLER" /D "BROKEN_SIGSUSPEND" /D "HAVE_GETHOSTNAME" /D "MKFIFO_MISSING" /D "NO_DEV_TTY_JOB_CONTROL" /D "NO_SBRK_DECL" /D "PGRP_PIPE" /D "TERMIOS_MISSING" /D "HAVE_DUP2" /D "HAVE_STRERROR" /D "HAVE_DIRENT" /D "HAVE_STRING_H" /D "HAVE_VARARGS_H" /D "HAVE_STRCHR" /D "SHELL" /D "HAVE_ALLOCA" /D "HAVE_ALLOCA_H" /D "WIN32" /D "_CONSOLE" /D "_MBCS" /YX /FD /GZ /c
# ADD BASE RSC /l 0x804 /d "_DEBUG"
# ADD RSC /l 0x804 /d "_DEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:console /debug /machine:I386 /pdbtype:sept
# ADD LINK32 kernel32.lib user32.lib Advapi32.lib /nologo /subsystem:console /debug /machine:I386 /out:"Debug/sh.exe" /pdbtype:sept

!ENDIF 

# Begin Target

# Name "Bash - Win32 Release"
# Name "Bash - Win32 Debug"
# Begin Group "Source Files"

# PROP Default_Filter "cpp;c;cxx;rc;def;r;odl;idl;hpj;bat"
# Begin Group "win32-subproc"

# PROP Default_Filter ""
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\win32-subproc\db_level.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\win32-subproc\misc.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\win32-subproc\proc.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\win32-subproc\sub_proc.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\win32-subproc\w32err.c"
# End Source File
# End Group
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\alias.c"
# End Source File
# Begin Source File

SOURCE=..\..\v01\dum_inc\bash_dum.c
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\bashhist.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\bashline.c"
# End Source File
# Begin Source File

SOURCE=..\..\v01\dum_inc\bcopy.c
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\bind.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\bracecomp.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\braces.c"
# End Source File
# Begin Source File

SOURCE=..\..\v01\dum_inc\bzero.c
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\complete.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\copy_cmd.c"
# End Source File
# Begin Source File

SOURCE=..\..\v01\dum_inc\dirent.c
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\display.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\dispose_cmd.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\error.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\execute_cmd.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\expr.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\flags.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\glob\fnmatch.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\glob\fnmatch.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\funmap.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\general.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\getcwd.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\glob\glob.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\hash.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\history.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\input.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\isearch.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\keymaps.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\mailcheck.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\make_cmd.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\glob\ndir.h"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\nojobs.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\nt_vc.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\parens.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\print_cmd.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\readline.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\rltty.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\search.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\shell.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\siglist.c"
# End Source File
# Begin Source File

SOURCE=..\..\v01\dum_inc\signal.c
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\signals.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\subst.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\test.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\tilde.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\trap.c"
# End Source File
# Begin Source File

SOURCE=..\..\v01\dum_inc\unistd.c
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\unwind_prot.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\variables.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\version.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\lib\readline\vi_mode.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\win32-extra.c"
# End Source File
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\y_tab.c"
# End Source File
# End Group
# Begin Group "Header Files"

# PROP Default_Filter "h;hpp;hxx;hm;inl"
# Begin Source File

SOURCE="..\..\v01\bash-1.14.2\win32-extra.h"
# End Source File
# End Group
# End Target
# End Project
