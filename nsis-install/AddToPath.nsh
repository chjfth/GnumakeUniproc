; [2007-03-02]
; From: http://nsis.sourceforge.net/Path_Manipulation
; with some modification

!ifndef _AddToPath_nsh
!define _AddToPath_nsh

!verbose 3
!include "WinMessages.NSH"
!verbose 4

!ifndef WriteEnvStr_RegKey
  !ifdef ALL_USERS
    !define WriteEnvStr_RegKey \
       'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"'
  !else
    !define WriteEnvStr_RegKey 'HKCU "Environment"'
  !endif
!endif

; AddToPath - Adds the given dir to the search path.
;    Input - 
;       * head-1 of the stack: the dir to add to PATH
;       * head of stack: whether add to front or rear. "front" for front, "rear" for rear.
;    Note - Win9x systems requires reboot
;
;[2007-03-04] Chj: Add a param to indicate whether add the new path at front
;or at rear of current PATH string. In order to accomplish the front/rear policy,
;special action is taken: If the input dir string is in PATH already, we remove it
;first before prepending/appending it to PATH -- instead of jumping to AddToPath_done.

!define AddToPath "!insertmacro AddToPath"
        ; This AddToPath hybrid technique is taught by http://nsis.sourceforge.net/Macro_vs_Function

!macro AddToPath DirToAdd front_or_rear
  Push "${DirToAdd}"
  Push "${front_or_rear}"
  Call AddToPath
!macroend
Function AddToPath
  Exch $4 ; result: "front" or "rear" in $4
  Exch
  Exch $0 ; result: input-dir in $0.         Stack: orig $0, orig $4, ...
  Push $1
  Push $2
  Push $3
;DetailPrint ">>>> $0, $4"
  # don't add if the path doesn't exist
  IfFileExists "$0\*.*" "" AddToPath_done ;[2007-03-02] Chj commented out

  ReadEnvStr $1 PATH
    ;[2007-03-02]Chj: This should better be retrieved from registry(NT) or autoexec.bat(98),
    ;not from current process. Hmm, but why he use
    ;    ReadRegStr $1 ${WriteEnvStr_RegKey} "PATH"
    ;below AddToPath_NT to load PATH value from registry again?
    ;[2007-03-04]Chj: Retrieving PATH value from current process may due to such
    ;consideration: If that dir has been set in "system-wide" PATH, then no need to set
    ;it again here. However, check system-area PATH setting in registry requires
    ;more code, which is boring.
    ;     Honestly, for a NSIS installer author, be aware of the impact of checking
    ;current process PATH here! If you(the NSIS installer author) launch the just
    ;built installer from HM SIS Editor, the PATH retrieved may be different from
    ;what is the current in the registry. Therefore, if your installer alters PATH,
    ;you'd better launch the test installer from explorer process(and NOTE, the desktop
    ;explorer process, not the "extra" one -- if you told Windows to use two explorer
    ;process). The evil reason for such situation: It seems no programs would like to
    ;[process WM_WININICHANGE or WM_SETTINGCHANGE and reload PATH env-var] except
    ;Windows desktop explorer process.

  Push "$1;" ; Chj: Note the semicolon at the end, it's wise.
  Push "$0;"
  Call StrStr
  Pop $2
;DetailPrint "a1 (PATH;). $1;"
;DetailPrint "a2(input;). $0;"
;DetailPrint "a3(found). $2"
  StrCmp $2 "" FindPathExisting_bkslashend ""
  Push "$0" ; RemoveFromPath's param. Yes, use "$0", not "$0;", since RemoveFromPath don't expect the semicolon
  Call RemoveFromPath
FindPathExisting_bkslashend:
  Push "$1;"
  Push "$0\;"
  Call StrStr
  Pop $2
;DetailPrint "b. $2"
  StrCmp $2 "" FindShortPathExisting ""
;DetailPrint "bb. $$0 = $0"
  Push "$0\"
  Call RemoveFromPath
FindShortPathExisting:
  GetFullPathName /SHORT $3 $0
;DetailPrint "bb. $$3 = $3"
  Push "$1;"
  Push "$3;"
  Call StrStr
  Pop $2
;DetailPrint "c. $2"
  StrCmp $2 "" FindShortPathExisting_bkslashend ""
  Push "$3" ; RemoveFromPath's param
  Call RemoveFromPath
FindShortPathExisting_bkslashend:
  Push "$1;"
  Push "$3\;"
  Call StrStr
  Pop $2
;DetailPrint "d. $2"
  StrCmp $2 "" RemovedInputPathFromExistingPATH ""
  Push "$3\" ; RemoveFromPath's param
  Call RemoveFromPath

RemovedInputPathFromExistingPATH:

  Call IsNT
  Pop $1
  StrCmp $1 1 AddToPath_NT
    ; Not on NT
    StrCpy $1 $WINDIR 2
    FileOpen $1 "$1\autoexec.bat" a
    FileSeek $1 -1 END
    FileReadByte $1 $2
    IntCmp $2 26 0 +2 +2 # DOS EOF
      FileSeek $1 -1 END # write over EOF
    StrCmp "$4" "front" "" AddToPath_rear_NotNT
      FileWrite $1 "$\r$\nSET PATH=$3;%PATH%$\r$\n"
      Goto AddToPath_NotNT_done
    AddToPath_rear_NotNT:
      FileWrite $1 "$\r$\nSET PATH=%PATH%;$3$\r$\n"
    AddToPath_NotNT_done:
    FileClose $1
    SetRebootFlag true
    Goto AddToPath_done

  AddToPath_NT:
    ReadRegStr $1 ${WriteEnvStr_RegKey} "PATH"
    StrCmp $1 "" AddToPath_NTdoIt
      Push $1
      Call Trim
      Pop $1
      StrCmp "$4" "front" "" AddToPath_rear_NT
        StrCpy $0 "$0;$1"
        Goto AddToPath_NTdoIt
    AddToPath_rear_NT:
        StrCpy $0 "$1;$0"
    AddToPath_NTdoIt:
      WriteRegExpandStr ${WriteEnvStr_RegKey} "PATH" $0
      SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
;DetailPrint "AtPRe: $0" ;this for test

  AddToPath_done:
    Pop $3
    Pop $2
    Pop $1
    Pop $0
    Pop $4
FunctionEnd

; RemoveFromPath - Remove a given dir from the path
;     Input: head of the stack
!macro RemoveFromPath UN
Function ${UN}RemoveFromPath
  Exch $0
  Push $1
  Push $2
  Push $3
  Push $4
  Push $5
  Push $6

  IntFmt $6 "%c" 26 # DOS EOF

  Call ${UN}IsNT
  Pop $1
  StrCmp $1 1 unRemoveFromPath_NT
    ; Not on NT
    StrCpy $1 $WINDIR 2
    FileOpen $1 "$1\autoexec.bat" r
    GetTempFileName $4
    FileOpen $2 $4 w
    GetFullPathName /SHORT $0 $0
    StrCpy $0 "SET PATH=%PATH%;$0"
    Goto unRemoveFromPath_dosLoop

    unRemoveFromPath_dosLoop:
      FileRead $1 $3
      StrCpy $5 $3 1 -1 # read last char
      StrCmp $5 $6 0 +2 # if DOS EOF
        StrCpy $3 $3 -1 # remove DOS EOF so we can compare
      StrCmp $3 "$0$\r$\n" unRemoveFromPath_dosLoopRemoveLine
      StrCmp $3 "$0$\n" unRemoveFromPath_dosLoopRemoveLine
      StrCmp $3 "$0" unRemoveFromPath_dosLoopRemoveLine
      StrCmp $3 "" unRemoveFromPath_dosLoopEnd
      FileWrite $2 $3
      Goto unRemoveFromPath_dosLoop
      unRemoveFromPath_dosLoopRemoveLine:
        SetRebootFlag true
        Goto unRemoveFromPath_dosLoop

    unRemoveFromPath_dosLoopEnd:
      FileClose $2
      FileClose $1
      StrCpy $1 $WINDIR 2
      Delete "$1\autoexec.bat"
      CopyFiles /SILENT $4 "$1\autoexec.bat"
      Delete $4
      Goto unRemoveFromPath_done

  unRemoveFromPath_NT:
    ReadRegStr $1 ${WriteEnvStr_RegKey} "PATH"
    StrCpy $5 $1 1 -1 # copy last char
    StrCmp $5 ";" +2 # if last char != ;
      StrCpy $1 "$1;" # append ;
    Push $1
    Push "$0;"
    Call ${UN}StrStr ; Find `$0;` in $1
    Pop $2 ; pos of our dir
    StrCmp $2 "" unRemoveFromPath_done
      ; else, it is in path
      # $0 - path to add
      # $1 - path var
      StrLen $3 "$0;"
      StrLen $4 $2
      StrCpy $5 $1 -$4 # $5 is now the part before the path to remove
      StrCpy $6 $2 "" $3 # $6 is now the part after the path to remove
      StrCpy $3 $5$6

      StrCpy $5 $3 1 -1 # copy last char
      StrCmp $5 ";" 0 +2 # if last char == ;
        StrCpy $3 $3 -1 # remove last char

      WriteRegExpandStr ${WriteEnvStr_RegKey} "PATH" $3
      SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000

  unRemoveFromPath_done:
    Pop $6
    Pop $5
    Pop $4
    Pop $3
    Pop $2
    Pop $1
    Pop $0
FunctionEnd
!macroend
!insertmacro RemoveFromPath ""
!insertmacro RemoveFromPath "un."

; AddToEnvVar - Adds the given value to the given environment var
;        Input - head of the stack $0 environement variable $1=value to add
;        Note - Win9x systems requires reboot

Function AddToEnvVar

  Exch $1 ; $1 has environment variable value
  Exch
  Exch $0 ; $0 has environment variable name

  DetailPrint "Adding $1 to $0"
  Push $2
  Push $3
  Push $4


  ReadEnvStr $2 $0
  Push "$2;"
  Push "$1;"
  Call StrStr
  Pop $3
  StrCmp $3 "" "" AddToEnvVar_done

  Push "$2;"
  Push "$1\;"
  Call StrStr
  Pop $3
  StrCmp $3 "" "" AddToEnvVar_done


  Call IsNT
  Pop $2
  StrCmp $2 1 AddToEnvVar_NT
    ; Not on NT
    StrCpy $2 $WINDIR 2
    FileOpen $2 "$2\autoexec.bat" a
    FileSeek $2 -1 END
    FileReadByte $2 $3
    IntCmp $3 26 0 +2 +2 # DOS EOF
      FileSeek $2 -1 END # write over EOF
    FileWrite $2 "$\r$\nSET $0=%$0%;$4$\r$\n"
    FileClose $2
    SetRebootFlag true
    Goto AddToEnvVar_done

  AddToEnvVar_NT:
    ReadRegStr $2 ${WriteEnvStr_RegKey} $0
    StrCpy $3 $2 1 -1 # copy last char
    StrCmp $3 ";" 0 +2 # if last char == ;
      StrCpy $2 $2 -1 # remove last char
    StrCmp $2 "" AddToEnvVar_NTdoIt
      StrCpy $1 "$2;$1"
    AddToEnvVar_NTdoIt:
      WriteRegExpandStr ${WriteEnvStr_RegKey} $0 $1
      SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000

  AddToEnvVar_done:
    Pop $4
    Pop $3
    Pop $2
    Pop $0
    Pop $1

FunctionEnd

; RemoveFromEnvVar - Remove a given value from a environment var
;     Input: head of the stack

!macro RemoveFromEnvVar UN
Function ${UN}RemoveFromEnvVar

  Exch $1 ; $1 has environment variable value
  Exch
  Exch $0 ; $0 has environment variable name

  DetailPrint "Removing $1 from $0"
  Push $2
  Push $3
  Push $4
  Push $5
  Push $6
  Push $7

  IntFmt $7 "%c" 26 # DOS EOF

  Call ${UN}IsNT
  Pop $2
  StrCmp $2 1 unRemoveFromEnvVar_NT
    ; Not on NT
    StrCpy $2 $WINDIR 2
    FileOpen $2 "$2\autoexec.bat" r
    GetTempFileName $5
    FileOpen $3 $5 w
    GetFullPathName /SHORT $1 $1
    StrCpy $1 "SET $0=%$0%;$1"
    Goto unRemoveFromEnvVar_dosLoop

    unRemoveFromEnvVar_dosLoop:
      FileRead $2 $4
      StrCpy $6 $4 1 -1 # read last char
      StrCmp $6 $7 0 +2 # if DOS EOF
        StrCpy $4 $4 -1 # remove DOS EOF so we can compare
      StrCmp $4 "$1$\r$\n" unRemoveFromEnvVar_dosLoopRemoveLine
      StrCmp $4 "$1$\n" unRemoveFromEnvVar_dosLoopRemoveLine
      StrCmp $4 "$1" unRemoveFromEnvVar_dosLoopRemoveLine
      StrCmp $4 "" unRemoveFromEnvVar_dosLoopEnd
      FileWrite $3 $4
      Goto unRemoveFromEnvVar_dosLoop
      unRemoveFromEnvVar_dosLoopRemoveLine:
        SetRebootFlag true
        Goto unRemoveFromEnvVar_dosLoop

    unRemoveFromEnvVar_dosLoopEnd:
      FileClose $3
      FileClose $2
      StrCpy $2 $WINDIR 2
      Delete "$2\autoexec.bat"
      CopyFiles /SILENT $5 "$2\autoexec.bat"
      Delete $5
      Goto unRemoveFromEnvVar_done

  unRemoveFromEnvVar_NT:
    ReadRegStr $2 ${WriteEnvStr_RegKey} $0
    StrCpy $6 $2 1 -1 # copy last char
    StrCmp $6 ";" +2 # if last char != ;
      StrCpy $2 "$2;" # append ;
    Push $2
    Push "$1;"
    Call ${UN}StrStr ; Find `$1;` in $2
    Pop $3 ; pos of our dir
    StrCmp $3 "" unRemoveFromEnvVar_done
      ; else, it is in path
      # $1 - path to add
      # $2 - path var
      StrLen $4 "$1;"
      StrLen $5 $3
      StrCpy $6 $2 -$5 # $6 is now the part before the path to remove
      StrCpy $7 $3 "" $4 # $7 is now the part after the path to remove
      StrCpy $4 $6$7

      StrCpy $6 $4 1 -1 # copy last char
      StrCmp $6 ";" 0 +2 # if last char == ;
      StrCpy $4 $4 -1 # remove last char

      WriteRegExpandStr ${WriteEnvStr_RegKey} $0 $4

      ; delete reg value if null
      StrCmp $4 "" 0 +2 # if null delete reg
      DeleteRegValue ${WriteEnvStr_RegKey} $0

      SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000

  unRemoveFromEnvVar_done:
    Pop $7
    Pop $6
    Pop $5
    Pop $4
    Pop $3
    Pop $2
    Pop $1
    Pop $0
FunctionEnd
!macroend
!insertmacro RemoveFromEnvVar ""
!insertmacro RemoveFromEnvVar "un."



!ifndef IsNT_KiCHiK
!define IsNT_KiCHiK

###########################################
#            Utility Functions            #
###########################################

; IsNT
; no input
; output, top of the stack = 1 if NT or 0 if not
;
; Usage:
;   Call IsNT
;   Pop $R0
;  ($R0 at this point is 1 or 0)

!macro IsNT un
Function ${un}IsNT
  Push $0
  ReadRegStr $0 HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion
  StrCmp $0 "" 0 IsNT_yes
  ; we are not NT.
  Pop $0
  Push 0
  Return

  IsNT_yes:
    ; NT!!!
    Pop $0
    Push 1
FunctionEnd
!macroend
!insertmacro IsNT ""
!insertmacro IsNT "un."

!endif ; IsNT_KiCHiK

; StrStr
; input, top of stack = string to search for
;        top of stack-1 = string to search in
; output, top of stack (replaces with the portion of the string remaining)
; modifies no other variables.
;
; Usage:
;   Push "this is a long ass string"
;   Push "ass"
;   Call StrStr
;   Pop $R0
;  ($R0 at this point is "ass string")

!macro StrStr un
Function ${un}StrStr
Exch $R1 ; st=haystack,old$R1, $R1=needle
  Exch    ; st=old$R1,haystack
  Exch $R2 ; st=old$R1,old$R2, $R2=haystack
  Push $R3
  Push $R4
  Push $R5
  StrLen $R3 $R1
  StrCpy $R4 0
  ; $R1=needle
  ; $R2=haystack
  ; $R3=len(needle)
  ; $R4=cnt
  ; $R5=tmp
  loop:
    StrCpy $R5 $R2 $R3 $R4
    StrCmp $R5 $R1 done
    StrCmp $R5 "" done
    IntOp $R4 $R4 + 1
    Goto loop
done:
  StrCpy $R1 $R2 "" $R4
  Pop $R5
  Pop $R4
  Pop $R3
  Pop $R2
  Exch $R1
FunctionEnd
!macroend
!insertmacro StrStr ""
!insertmacro StrStr "un."

!endif ; _AddToPath_nsh

Function Trim ; Added by Pelaca
	Exch $R1
	Push $R2
Loop:
	StrCpy $R2 "$R1" 1 -1
	StrCmp "$R2" " " RTrim
	StrCmp "$R2" "$\n" RTrim
	StrCmp "$R2" "$\r" RTrim
	StrCmp "$R2" ";" RTrim
	GoTo Done
RTrim:
	StrCpy $R1 "$R1" -1
	Goto Loop
Done:
	Pop $R2
	Exch $R1
FunctionEnd
