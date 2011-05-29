;
; For a param `varname'
; Variable isChecked_${varname} tells whether this env-var should be set or deleted
; Variable str_${varname} tells the value of that env-var
!macro DoStoreEnvVar varname
  Push "${varname}"
  ${If} "$isStoreEnvVarToRegistry" == 1
  ${AndIf} "$isChecked_${varname}" == 1
      Push "$str_${varname}"
      Call WriteEnvStr
  ${Else}
      Call DeleteEnvStr
  ${EndIf}
  
  ${If} "$isStoreEnvVarToBat" == 1
  ${AndIf} "$isChecked_${varname}" == 1
    Push $4
    FileOpen $4 "${fpath_GmuEnvBat}" a
    FileSeek $4 0 END
    FileWrite $4 "$\r$\n" ; we write a new line
    
    ; Replace D:/GMU and D:\GMU\ to env-var substitution form.
    !insertmacro ReplaceSubStr "SET ${varname}=$str_${varname}" "$InstDir_fwslash" "%gmu_DIR_ROOT%"
;	DetailPrint ">>!>> $R0...$INSTDIR\"
;	!insertmacro ReplaceSubStr "$R0" "$INSTDIR" "%gmu_DIR_ROOT_bs%"
    
    FileWrite $4 "$R0"
    FileWrite $4 "$\r$\n" ; we write an extra line
    FileClose $4 ; and close the file
    Pop $4
  ${EndIf}
!macroend

!macro AddBat_gmu_goody
  ${If} "$isStoreEnvVarToBat" == 1
    Push $4
    FileOpen $4 "${fpath_GmuEnvBat}" a
    FileSeek $4 0 END
    FileWrite $4 "$\r$\n" ; we write a new line
    FileWrite $4 "call %gmu_DIR_ROOT_bs%\%MinGW2\bin\gmu-goody.bat"
    FileWrite $4 "$\r$\n" ; we write an extra line
    FileClose $4 ; and close the file
    Pop $4
  ${EndIf}
!macroend

!macro DoStoreEnvVar_list v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 ;v11 v12 v13
  !insertmacro DoStoreEnvVar ${v1}
  !insertmacro DoStoreEnvVar ${v2}
  !insertmacro DoStoreEnvVar ${v3}
  !insertmacro DoStoreEnvVar ${v4}
  !insertmacro DoStoreEnvVar ${v5}
  !insertmacro DoStoreEnvVar ${v6}
  !insertmacro DoStoreEnvVar ${v7}
  !insertmacro DoStoreEnvVar ${v8}
  !insertmacro DoStoreEnvVar ${v9}
  !insertmacro DoStoreEnvVar ${v10}
;  !insertmacro DoStoreEnvVar ${v11}
;  !insertmacro DoStoreEnvVar ${v12}
;  !insertmacro DoStoreEnvVar ${v13}
!macroend

!macro DoAddPathEnvVar varname
  ${If} "$isStoreEnvVarToRegistry" == 1
  ${AndIf} "$isChecked_${varname}" == 1
    Push $0 ; save $0
    ${If} "$isAddToPathFront" == 1
      StrCpy $0 "front" ; modify $0
    ${Else}
      StrCpy $0 "rear" ; modify $0
    ${EndIf}
    ${AddToPath} "$str_${varname}" $0
    Pop $0 ; restore $0
  ${Else}
    Push "$str_${varname}"
    Call RemoveFromPath
  ${EndIf}

  ${If} "$isStoreEnvVarToBat" == 1
    Push $4
    FileOpen $4 "${fpath_GmuEnvBat}" a
    FileSeek $4 0 END
    FileWrite $4 "$\r$\n" ; we write a new line
    ${If} "$isAddToPathFront" == 1
      StrCpy $R1 "SET PATH=$str_${varname};%PATH%"
    ${Else}
      StrCpy $R1 "SET PATH=%PATH%;$str_${varname}"
    ${EndIf}
	!insertmacro ReplaceSubStr "$R1" "$INSTDIR" "%gmu_DIR_ROOT_bs%"
	FileWrite $4 "$R0"
    FileWrite $4 "$\r$\n" ; we write an extra line
    FileClose $4 ; and close the file
    Pop $4
  ${EndIf}
!macroend

;;; Delete env-var in registry

!macro un.DelRegistryEnvVar varname
  Push "${varname}"
  Call un.DeleteEnvStr
!macroend
!macro un.DelRegistryEnvVar_list v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 ;v11 v12 v13
  !insertmacro un.DelRegistryEnvVar ${v1}
  !insertmacro un.DelRegistryEnvVar ${v2}
  !insertmacro un.DelRegistryEnvVar ${v3}
  !insertmacro un.DelRegistryEnvVar ${v4}
  !insertmacro un.DelRegistryEnvVar ${v5}
  !insertmacro un.DelRegistryEnvVar ${v6}
  !insertmacro un.DelRegistryEnvVar ${v7}
  !insertmacro un.DelRegistryEnvVar ${v8}
  !insertmacro un.DelRegistryEnvVar ${v9}
  !insertmacro un.DelRegistryEnvVar ${v10}
;  !insertmacro un.DelRegistryEnvVar ${v11}
;  !insertmacro un.DelRegistryEnvVar ${v12}
;  !insertmacro un.DelRegistryEnvVar ${v13}
!macroend

;;; Append env-vardefines to $R0

!macro AppendEnvVarDef_R0 varname
  ${If} "$isChecked_${varname}" == 1
    StrCpy "$R0" "$R0${varname}=$str_${varname}\r\n        ${desc_${varname}}\r\n\r\n"
    ; Really, you cannot write $\r for \r here!
  ${EndIf}
!macroend

!macro AppendEnvVarDef_R0_list v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 ;v11 v12 v13
  !insertmacro AppendEnvVarDef_R0 ${v1}
  !insertmacro AppendEnvVarDef_R0 ${v2}
  !insertmacro AppendEnvVarDef_R0 ${v3}
  !insertmacro AppendEnvVarDef_R0 ${v4}
  !insertmacro AppendEnvVarDef_R0 ${v5}
  !insertmacro AppendEnvVarDef_R0 ${v6}
  !insertmacro AppendEnvVarDef_R0 ${v7}
  !insertmacro AppendEnvVarDef_R0 ${v8}
  !insertmacro AppendEnvVarDef_R0 ${v9}
  !insertmacro AppendEnvVarDef_R0 ${v10}
;  !insertmacro AppendEnvVarDef_R0 ${v11}
;  !insertmacro AppendEnvVarDef_R0 ${v12}
;  !insertmacro AppendEnvVarDef_R0 ${v13}
!macroend

;;;

!macro BkslashToFwslash varname
  Push '$str_${varname}'
  Push "\"
  Call StrSlash
  Pop '$str_${varname}'
!macroend

!macro BkslashToFwslash_list v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 ;v11 v12 v13
  !insertmacro BkslashToFwslash ${v1}
  !insertmacro BkslashToFwslash ${v2}
  !insertmacro BkslashToFwslash ${v3}
  !insertmacro BkslashToFwslash ${v4}
  !insertmacro BkslashToFwslash ${v5}
  !insertmacro BkslashToFwslash ${v6}
  !insertmacro BkslashToFwslash ${v7}
  !insertmacro BkslashToFwslash ${v8}
  !insertmacro BkslashToFwslash ${v9}
  !insertmacro BkslashToFwslash ${v10}
;  !insertmacro BkslashToFwslash ${v11}
;  !insertmacro BkslashToFwslash ${v12}
;  !insertmacro BkslashToFwslash ${v13}
!macroend

;;;
