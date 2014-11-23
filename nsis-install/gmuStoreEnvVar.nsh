;
; For a param `varname'
; Variable isChecked_${varname} tells whether this env-var should be set or deleted
; Variable str_${varname} tells the value of that env-var
!macro DoStoreEnvVar varname
  Push "${varname}"
  ${If} "$isChecked_${varname}" == 1
      Push "$str_${varname}"
      Call WriteEnvStr
  ${Else}
      Call DeleteEnvStr
  ${EndIf}  
!macroend


!macro DoStoreEnvVar_list v1 v2 ;v3 v4 v5 v6 v7 v8 v9 v10 v11 v12 v13
  !insertmacro DoStoreEnvVar ${v1}
  !insertmacro DoStoreEnvVar ${v2}
;  !insertmacro DoStoreEnvVar ${v3}
;  !insertmacro DoStoreEnvVar ${v4}
;  !insertmacro DoStoreEnvVar ${v5}
;  !insertmacro DoStoreEnvVar ${v6}
;  !insertmacro DoStoreEnvVar ${v7}
;  !insertmacro DoStoreEnvVar ${v8}
;  !insertmacro DoStoreEnvVar ${v9}
;  !insertmacro DoStoreEnvVar ${v10}
;  !insertmacro DoStoreEnvVar ${v11}
;  !insertmacro DoStoreEnvVar ${v12}
;  !insertmacro DoStoreEnvVar ${v13}
!macroend

!macro DoAddPathEnvVar partial_varname
  ${If} "$isChecked_${partial_varname}" == 1
    Push $0 ; save $0
    ${If} "$isAddToPathFront" == 1
      StrCpy $0 "front" ; modify $0
    ${Else}
      StrCpy $0 "rear" ; modify $0
    ${EndIf}
    DetailPrint "Adding to PATH: $str_${partial_varname} ..."
    ${AddToPath} "$str_${partial_varname}" $0
    Pop $0 ; restore $0
  ${Else}
    ${If} "$str_${partial_varname}" != ""
      DetailPrint "Removing from PATH: $str_${partial_varname} ..."
      Push "$str_${partial_varname}"
      Call RemoveFromPath
    ${EndIf}
  ${EndIf}
!macroend

;;; Delete env-var in registry

!macro DelRegistryEnvVar varname
  Push "${varname}"
  Call DeleteEnvStr
!macroend
!macro DelRegistryEnvVar_list v1 v2 v3 v4 v5 v6 v7 v8 ;v9 v10 v11 v12 v13
  !insertmacro DelRegistryEnvVar ${v1}
  !insertmacro DelRegistryEnvVar ${v2}
  !insertmacro DelRegistryEnvVar ${v3}
  !insertmacro DelRegistryEnvVar ${v4}
  !insertmacro DelRegistryEnvVar ${v5}
  !insertmacro DelRegistryEnvVar ${v6}
  !insertmacro DelRegistryEnvVar ${v7}
  !insertmacro DelRegistryEnvVar ${v8}
;  !insertmacro DelRegistryEnvVar ${v9}
;  !insertmacro DelRegistryEnvVar ${v10}
;  !insertmacro DelRegistryEnvVar ${v11}
;  !insertmacro DelRegistryEnvVar ${v12}
;  !insertmacro DelRegistryEnvVar ${v13}
!macroend

;;; Append env-vardefines to $R0

!macro BkslashToFwslash varname
  Push '$str_${varname}'
  Push "\"
  Call StrSlash
  Pop '$str_${varname}'
!macroend

!macro BkslashToFwslash_list v1 v2 ;v3 v4 v5 v6 v7 v8 v9 v10 v11 v12 v13
  !insertmacro BkslashToFwslash ${v1}
  !insertmacro BkslashToFwslash ${v2}
;  !insertmacro BkslashToFwslash ${v3}
;  !insertmacro BkslashToFwslash ${v4}
;  !insertmacro BkslashToFwslash ${v5}
;  !insertmacro BkslashToFwslash ${v6}
;  !insertmacro BkslashToFwslash ${v7}
;  !insertmacro BkslashToFwslash ${v8}
;  !insertmacro BkslashToFwslash ${v9}
;  !insertmacro BkslashToFwslash ${v10}
;  !insertmacro BkslashToFwslash ${v11}
;  !insertmacro BkslashToFwslash ${v12}
;  !insertmacro BkslashToFwslash ${v13}
!macroend

;;;
