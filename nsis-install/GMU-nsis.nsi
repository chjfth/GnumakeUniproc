; Script generated by the HM NIS Edit Script Wizard.

SetCompressor /solid lzma

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "LogicLib.nsh"

!include "StrSlash.nsh"
!include "WriteEnvStr.nsh"
!include "AddToPath.nsh"

!include "gmuStoreEnvVar.nsh"

; My const defines for GnumakeUniproc install
!define fname_GmuEnvIni gmu-envvar.ini

!define dirname_MinGW MinGW2
!define suffix_dir_GMUext /GMU-ext
!define suffix_dir_ExtraCccfg /nlscan
!define suffix_dir_GMUbin \${dirname_MinGW}\bin
!define absdir_MinGW_bin_bkslash "$INSTDIR${suffix_dir_GMUbin}"
!define suffix_wincmd \GMU-main\umake_cmd\wincmd
!define absdir_wincmd "$INSTDIR${suffix_wincmd}"
!define uninst_exe_name "uninst-gmu.exe"
!define fpath_QuickStartGuide "$INSTDIR\GMU-manual\quick-start\quick-start.htm"

; My vars for GnumakeUniproc install

!define list_StaleGmuEnvVar "gmu_DIR_ROOT gmu_DIR_GNUMAKEUNIPROC gmu_ver \
    gmp_ud_list_CUSTOM_MKI gmp_ud_list_CUSTOM_COMPILER_CFG \
    gmp_DECO_PRJ_NAME \
    gmu_LOG_OUTPUT_FILENAME \
    gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING \
    "

Var isNewInstall
Var isAddToPathFront ; 1 means add-to-front, 0 means add-to-rear
Var isAddPath

Var isChecked_AddWincmdPath
      Var str_AddWincmdPath
Var isChecked_AddMingwPath ; Keep it null, so that D:\GMU\MinGW2\bin does not go into PATH
      Var str_AddMingwPath

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "GnumakeUniproc"
!define GMU_VER "0.101"
!define PRODUCT_VERSION "${GMU_VER}"
!define PRODUCT_PUBLISHER "Jimm Chen (chjfth@gmail.com)"
!define PRODUCT_WEB_SITE "http://gnumakeuniproc.sourceforge.net"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

!define PRODUCT_INST_ROOT_KEY "HKCU" ;[2006-05-08]Chj
!define PRODUCT_INST_KEY "Software\${PRODUCT_NAME}"


; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\orange-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\orange-uninstall.ico"

!define MUI_FINISHPAGE_NOAUTOCLOSE
; // Lauch something after install finished, according to
; http://nsis.sourceforge.net/Run_an_application_shortcut_after_an_install
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Read Quick start guide(html)."
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchQuickStartGuide"

!define MUI_COMPONENTSPAGE_SMALLDESC

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Component selection page
;!define MUI_COMPONENTSPAGE_SMALLDESC [2007-10-04]NSIS v2.24, !define this here will have no effect.
!insertmacro MUI_PAGE_COMPONENTS
Page custom SelectEnvVar
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!insertmacro MUI_PAGE_FINISH ; If not MUI_FINISHPAGE_NOAUTOCLOSE, removing this will keep the information output window.


; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS


; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "setup-gmu-v${GMU_VER}.exe"
InstallDir "D:\GMU" ; The default install dir
	
RequestExecutionLevel user ;Request application(not Administrator) privileges for Windows Vista+
ShowInstDetails show
ShowUnInstDetails show


ReserveFile "${NSISDIR}\Plugins\InstallOptions.dll" ; opt maybe
ReserveFile "${fname_GmuEnvIni}" ; opt maybe

!macro CopyASubdir subdir
  SetOutPath "$INSTDIR\${subdir}"
  File /r "nsis-data\${subdir}\*.*"
!macroend

!macro CopyASubdir_InGMU subdir
  SetOutPath "$INSTDIR\${subdir}"
  File /r "nsis-data\GMU\${subdir}\*.*"
!macroend

!macro ReadRegistryCfg cfgname
  ReadRegStr "$R0" ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}" ${cfgname}
  ; [2014-11-21] Now return value in $R0. Any other way to return?
!macroend

!macro MarkSectionByRegistry SectionName_nq ; nq: no double-quotes
  !insertmacro ReadRegistryCfg "${SectionName_nq}"

    ${If} "$R0" == "0"
      SectionSetFlags ${${SectionName_nq}} 0
    ${EndIf}
!macroend

!macro WriteRegistryCfg cfgname cfgval
  WriteRegStr ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}" ${cfgname} ${cfgval}
!macroend

!macro SaveRegistryBySectionMark SectionName_nq ; nq: no double-quotes
  SectionGetFlags ${${SectionName_nq}} $0
  IntOp $0 $0 & 1
  !insertmacro WriteRegistryCfg "${SectionName_nq}" "$0"
!macroend

; ========= sections start ===========

Section "GnumakeUniproc core scripts" GMU ; GnumakeUniproc required files
  SectionIn RO
  SetOverwrite try

  ; >>> nlscan specific. Remove any stale Scalacon template files.
  RMDir /r "$INSTDIR\nlscan\cprjtmpl"
  ; >>> nlscan specific.

  SetOutPath "$INSTDIR"
  File "nsis-data\GMU\*.txt"
  File "nsis-data\GMU\*.bat"
  File /nonfatal "nsis-data\GMU\*.htm"
  File /nonfatal "nsis-data\GMU\*.html"
  
  !insertmacro CopyASubdir_InGMU GMU-main
  !insertmacro CopyASubdir_InGMU GMU-ext
SectionEnd

Section "Necessary executables for GnumakeUniproc" NeceExes
  SectionIn RO
  SetOutPath "$INSTDIR${suffix_wincmd}"
  SetOverwrite try
  File /r "nsis-data\bin-gmu\*.*"

SectionEnd

Section /o "MinGW compiler(2.0) with gcc-3.2" MinGW
  SetOverwrite try
  !insertmacro CopyASubdir ${dirname_MinGW}
SectionEnd

Section "Additional executables for GnumakeUniproc" AddonExes
  SetOutPath "$INSTDIR${suffix_wincmd}"
  SetOverwrite try
  File /r "nsis-data\bin-gmu-addons\*.*"
SectionEnd

Section "Developer files(docs & examples etc)" DevFiles
  SetOutPath "$INSTDIR"
  SetOverwrite try
  !insertmacro CopyASubdir_InGMU GMU-manual
  !insertmacro CopyASubdir_InGMU GMU-examples
  !insertmacro CopyASubdir_InGMU demo-repositories
  !insertmacro CopyASubdir_InGMU nsis-install
  !insertmacro CopyASubdir_InGMU extras

  !insertmacro CopyASubdir_InGMU nlscan
SectionEnd


Section -AddEnvVars

  ; Deal with PATH env-var
  ${If} "$isAddToPathFront" == 1
    !insertmacro DoAddPathEnvVar AddMingwPath
    !insertmacro DoAddPathEnvVar AddWincmdPath
  ${Else}
    !insertmacro DoAddPathEnvVar AddWincmdPath
    !insertmacro DoAddPathEnvVar AddMingwPath
  ${EndIf}
  
  ; Record install target dir in registry
  WriteRegStr ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}" "InstallTargetDir" "$INSTDIR"
  DetailPrint "Writing registry key: [${PRODUCT_INST_ROOT_KEY}\${PRODUCT_INST_KEY}] InstallTargetDir=$INSTDIR"

  ; Remove stale GMU env-vars in registry from GMU v0.98.1 and earlier 
  !insertmacro DelRegistryEnvVar_list ${list_StaleGmuEnvVar}
  
  call BroadcastWinIniChange

SectionEnd


Section -AdditionalIcons
  ; HM SIS Edit v2.0.3 wizard geneated >>>
  CreateDirectory "$SMPROGRAMS\-GnumakeUniproc-"
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\-GnumakeUniproc-\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\-GnumakeUniproc-\Uninstall GMU.lnk" "$INSTDIR\${uninst_exe_name}"
  ; HM SIS Edit v2.0.3 wizard geneated <<<

  WriteIniStr "$INSTDIR\Quick start guide.url" "InternetShortcut" "URL" "${fpath_QuickStartGuide}"
  CreateShortCut "$SMPROGRAMS\-GnumakeUniproc-\Quick start guide.lnk" "$INSTDIR\Quick start guide.url"
;  WriteIniStr "$SMPROGRAMS\-GnumakeUniproc-\Quick start guide.lnk" "InternetShortcut" "URL" "${fpath_QuickStartGuide}"
   ;[2007-03-04]It seems this will not generate an INI style .lnk file. This .lnk file always has binary data. Why?
SectionEnd

Section -Post

  !insertmacro SaveRegistryBySectionMark MinGW
  !insertmacro SaveRegistryBySectionMark AddonExes
  !insertmacro SaveRegistryBySectionMark DevFiles

  WriteUninstaller "$INSTDIR\${uninst_exe_name}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\${uninst_exe_name}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_GMU ${LANG_ENGLISH} "GnumakeUniproc itself, including core make-partial files(.mki), and plugin files."
  LangString DESC_NeceExes ${LANG_ENGLISH} "Necessary Windows executables(sh.exe, mkdir.exe, etc) for running GnumakeUniproc."
  LangString DESC_MinGW ${LANG_ENGLISH} "Only for GMU demonstration purpose, not a must if you have your own compilers(MSVC etc)."
  LangString DESC_AddonExes ${LANG_ENGLISH} "Optional Windows executables that do some assistant work."
  LangString DESC_DevFiles ${LANG_ENGLISH} "Files for GMU developers, including documents, GMU examples projects, GMU templates etc."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${MinGW} $(DESC_MinGW)
    !insertmacro MUI_DESCRIPTION_TEXT ${GMU} $(DESC_GMU)
    !insertmacro MUI_DESCRIPTION_TEXT ${NeceExes} $(DESC_NeceExes)
    !insertmacro MUI_DESCRIPTION_TEXT ${AddonExes} $(DESC_AddonExes)
    !insertmacro MUI_DESCRIPTION_TEXT ${DevFiles} $(DESC_DevFiles)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Function .onInit

  ;Check Win9x
  Call IsNT
  Pop $R0
  ${If} "$R0" == 0
    MessageBox MB_YESNO "GnumakeUniproc does not support Windows 95/98/ME. Do you still want to install?" IDYES NoAbort
    Abort
  ${EndIf}
NoAbort:

  ;Extract InstallOptions INI files
  !insertmacro MUI_INSTALLOPTIONS_EXTRACT "${fname_GmuEnvIni}"

 ;Check previous installation
  !insertmacro ReadRegistryCfg "InstallTargetDir"
  ${If} "$R0" != "" ; Previous install exists
    StrCpy $INSTDIR $R0
 
    !insertmacro MarkSectionByRegistry MinGW
    !insertmacro MarkSectionByRegistry AddonExes
    !insertmacro MarkSectionByRegistry DevFiles
    
    StrCpy $isNewInstall 0
  ${Else}
    StrCpy $isNewInstall 1
  ${EndIf}

FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 \
    "Are you sure you want to completely remove $(^Name) and all of its components? $\n$\n \
    ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! $\n \
    CAUTION: This will remove ALL content in your installation directory! $\n \
    ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! \
    " \
    IDYES +2
  Abort
FunctionEnd

Section Uninstall

  RMDir /r "$INSTDIR" ; This clears them all!

  RMDir /r "$SMPROGRAMS\-GnumakeUniproc-"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}"
;  SetAutoClose true
SectionEnd

Section un.RemoveEnvVars

  ; Deal with PATH env-var
  DetailPrint "Removing $\"${absdir_MinGW_bin_bkslash}$\" from PATH env-var..."
  push "${absdir_MinGW_bin_bkslash}"
  call un.RemoveFromPath

  DetailPrint "Removing $\"${absdir_wincmd}$\" from PATH env-var..."
  push "${absdir_wincmd}"
  call un.RemoveFromPath

  call un.BroadcastWinIniChange

SectionEnd


;;;;;;;;;;;;;;;
Function SelectEnvVar

  !insertmacro MUI_INSTALLOPTIONS_WRITE "${fname_GmuEnvIni}" "Field 12" "State" \
    "${absdir_wincmd}" ;"${absdir_wincmd};${absdir_MinGW_bin_bkslash}"

  !insertmacro MUI_HEADER_TEXT "Select environment variables(env-var) to modify" \
    "GnumakeUniproc requires no modification to your system in order to run, except some directory in your PATH env-var."

  !insertmacro MUI_INSTALLOPTIONS_DISPLAY "${fname_GmuEnvIni}"

  !insertmacro MUI_INSTALLOPTIONS_READ $isAddPath ${fname_GmuEnvIni} "Field 11" "State"
  ${If} "$isAddPath" == 1
    StrCpy "$isChecked_AddWincmdPath" "1"
    StrCpy        "$str_AddWincmdPath" "${absdir_wincmd}"
  ${EndIf}

  StrCpy "$isChecked_AddMingwPath"  "0" ; "0" to remove this PATH anyway(done in DoAddPathEnvVar)
  StrCpy        "$str_AddMingwPath"  "${absdir_MinGW_bin_bkslash}"

  !insertmacro MUI_INSTALLOPTIONS_READ $isAddToPathFront ${fname_GmuEnvIni} "Field 13" "State"

FunctionEnd


Function LaunchQuickStartGuide
  ExecShell "" "${fpath_QuickStartGuide}"
FunctionEnd
