; Script generated by the HM NIS Edit Script Wizard.

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "LogicLib.nsh"

!include "StrSlash.nsh"
!include "WriteEnvStr.nsh"
!include "AddToPath.nsh"

;!include "myconst.nsh"
!include "gmuStoreEnvVar.nsh"


; My const defines for GnumakeUniproc install
!define fname_GmuEnvIni gmu-envvar.ini
!define fname_StoreEnvIni store-envvar.ini
!define fname_SydoEnvIni gmi-sydo-envvar.ini

!define dirname_MinGW MinGW2
!define suffix_dir_GMUext /GMU-ext
!define suffix_dir_ExtraCccfg /nlscan
!define suffix_dir_GMUbin \${dirname_MinGW}\bin
!define absdir_MinGW_bin_bkslash "$INSTDIR${suffix_dir_GMUbin}"

!define fname_GmuEnvBat gmuenv.bat
!define fpath_GmuEnvBat "$INSTDIR\${fname_GmuEnvBat}"
!define absdir_GmuCore "$InstDir_fwslash/GMU-main/GnumakeUniproc"
!define absdir_DIR_GMU_PRG "$InstDir_fwslash/${dirname_MinGW}/bin"

!define fpath_QuickStartGuide "$INSTDIR\GMU-manual\quick-start\quick-start.htm"

!define list_GmuEnvVar "gmu_DIR_ROOT gmu_DIR_GNUMAKEUNIPROC \
    gmp_ud_list_CUSTOM_MKI gmp_ud_list_CUSTOM_COMPILER_CFG \
    gmp_DECO_PRJ_NAME \
    gmu_LOG_OUTPUT_FILENAME \
    gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING \
    NLSSVN gv1 gv2 \
	"

!define TSFX "" ;"__tsfx" ; test suffix

; My vars for GnumakeUniproc install

Var isNewInstall

Var isStoreEnvVarToRegistry
Var isStoreEnvVarToBat
Var isAddToPathFront ; 1 means add-to-front, 0 means add-to-rear

Var InstDir_fwslash ; Store forward-slash version of $INSTDIR

Var isChecked_gmu_DIR_ROOT ;No selection for isChecked_gmu_DIR_ROOT, take it always checked.
      Var str_gmu_DIR_ROOT
 !define desc_gmu_DIR_ROOT \
         "Tells where GnumakeUniproc is installed."
Var isChecked_gmu_DIR_GNUMAKEUNIPROC
      Var str_gmu_DIR_GNUMAKEUNIPROC
 !define desc_gmu_DIR_GNUMAKEUNIPROC \
         "Tells where GnumakeUniproc.mki resides."
Var isChecked_gmp_ud_list_CUSTOM_MKI
      Var str_gmp_ud_list_CUSTOM_MKI
 !define desc_gmp_ud_list_CUSTOM_MKI \
         "Directories of your custom-image-mki or plugins."
Var isChecked_gmp_ud_list_CUSTOM_COMPILER_CFG
      Var str_gmp_ud_list_CUSTOM_COMPILER_CFG
 !define desc_gmp_ud_list_CUSTOM_COMPILER_CFG \
         "Directories of your extra compiler configs."
Var isChecked_gmp_DECO_PRJ_NAME
      Var str_gmp_DECO_PRJ_NAME
 !define desc_gmp_DECO_PRJ_NAME \
         "Whether project-names are be decorated with compiler-id, compiler-ver etc. \
         It should be set if you'd like to compile your C/C++ programs with more than one compiler."
Var isChecked_gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING
      Var str_gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING
 !define desc_gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING \
         "A tweak for GNU make 3.81+. If set to 1, there will be no output of verbose message \
         $\"No such file or directory$\" when a file is not found by makefiles 'include' directive."
Var isChecked_gmu_LOG_OUTPUT_FILENAME
      Var str_gmu_LOG_OUTPUT_FILENAME
 !define desc_gmu_LOG_OUTPUT_FILENAME \
         "For umake*.bat, tell where to log the make screen output."

Var isChecked_NLSSVN
      Var str_NLSSVN
 !define desc_NLSSVN "This is the SVN repository root URL for NLSCAN."
Var isChecked_gv1
      Var str_gv1
 !define desc_gv1 ""
Var isChecked_gv2
      Var str_gv2
 !define desc_gv2 ""

Var isChecked_AddPath
      Var str_AddPath

Var isChecked_nlscanenv


!define desc_StoreEnvVar "You have two places to store the env-vars required by GnumakeUniproc(GMU):\r\n\
* First, write to local user's registry, so that these env-vars are ready after you logon into Windows.\r\n\
* Second, save the env-var settings to $INSTDIR\${fname_GmuEnvBat}, so that you can execute \
 ${fname_GmuEnvBat} to set them only when required. \r\n\r\n\
The following env-vars are to be stored: \r\n\r\n"

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "GnumakeUniproc"
!define PRODUCT_VERSION "0.97-pre13(20110516)"
!define PRODUCT_PUBLISHER "GnumakeUniproc's author"
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
; Componet selection page
;!define MUI_COMPONENTSPAGE_SMALLDESC [2007-10-04]NSIS v2.24, !define this here will have no effect.
!insertmacro MUI_PAGE_COMPONENTS
Page custom SelectEnvVar
#Page custom SelectGmiSydoEnvVar
Page custom StoreEnvVar
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
OutFile "setup-gmu.exe"
InstallDir "D:\GMU" ; The default install dir
ShowInstDetails show
ShowUnInstDetails show


ReserveFile "${NSISDIR}\Plugins\InstallOptions.dll" ; opt maybe
ReserveFile "${fname_GmuEnvIni}" ; opt maybe
ReserveFile "${fname_StoreEnvIni}" ; opt maybe
ReserveFile "${fname_SydoEnvIni}" ;opt maybe

!macro CopyASubdir subdir
  SetOutPath "$INSTDIR\${subdir}"
  File /r "nsis-data\${subdir}\*.*"
!macroend
!macro CopyASubdir_InGMU subdir
  SetOutPath "$INSTDIR\${subdir}"
  File /r "nsis-data\GMU\${subdir}\*.*"
!macroend

; ========= sections start ===========

Section "MinGW compiler(2.0) with gcc-3.2" MinGW
  SetOverwrite try
  !insertmacro CopyASubdir ${dirname_MinGW}
SectionEnd

Section "GnumakeUniproc" GMU ; GnumakeUniproc required files
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
  SetOutPath "$INSTDIR${suffix_dir_GMUbin}"
  SetOverwrite try
  File /r "nsis-data\bin-gmu\*.*"

  File "nsis-data\GMU\GMU-main\umake_cmd\wincmd\*.*"
SectionEnd

Section "Additional executables for GnumakeUniproc" AddonExes
  SetOutPath "$INSTDIR${suffix_dir_GMUbin}"
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
  !insertmacro CopyASubdir_InGMU nlscan
SectionEnd


Section -AddEnvVars

  DetailPrint "Storing GnumakeUniproc env-vars..."
  !insertmacro DoStoreEnvVar_list ${list_GmuEnvVar}

  ; Deal with PATH env-var
  DetailPrint "Adding PATH env-var..."
  !insertmacro DoAddPathEnvVar AddPath

  ; Add call D:\GMU\MinGW2\bin\gmu-goody.bat
  !insertmacro AddBat_gmu_goody

  ; Record install target dir in registry
  WriteRegStr ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}" "InstallTargetDir" "$INSTDIR"
  DetailPrint "Writing registry key: [${PRODUCT_INST_ROOT_KEY}\${PRODUCT_INST_KEY}] InstallTargetDir=$InstDir_fwslash"

  WriteRegStr ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}" "isStoreEnvVarToRegistry" "$isStoreEnvVarToRegistry"
  DetailPrint "Writing registry key: [${PRODUCT_INST_ROOT_KEY}\${PRODUCT_INST_KEY}] isStoreEnvVarToRegistry=$isStoreEnvVarToRegistry"


  call BroadcastWinIniChange

SectionEnd


Section -AdditionalIcons
  ; HM SIS Edit v2.0.3 wizard geneated >>>
  CreateDirectory "$SMPROGRAMS\-GnumakeUniproc-"
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\-GnumakeUniproc-\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\-GnumakeUniproc-\Uninstall.lnk" "$INSTDIR\uninst.exe"
  ; HM SIS Edit v2.0.3 wizard geneated <<<

  WriteIniStr "$INSTDIR\Quick start guide.url" "InternetShortcut" "URL" "${fpath_QuickStartGuide}"
  CreateShortCut "$SMPROGRAMS\-GnumakeUniproc-\Quick start guide.lnk" "$INSTDIR\Quick start guide.url"
;  WriteIniStr "$SMPROGRAMS\-GnumakeUniproc-\Quick start guide.lnk" "InternetShortcut" "URL" "${fpath_QuickStartGuide}"
   ;[2007-03-04]It seems this will not generate an INI style .lnk file. This .lnk file always has binary data. Why?
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_MinGW ${LANG_ENGLISH} "This includes mingw-gcc 3.2. It is optional if you have your own MinGW version."
  LangString DESC_GMU ${LANG_ENGLISH} "GnumakeUniproc itself, including core make-partial files(.mki), and plugin files."
  LangString DESC_NeceExes ${LANG_ENGLISH} "Necessary Windows executables(sh.exe, mkdir.exe, etc) for running GnumakeUniproc."
  LangString DESC_AddonExes ${LANG_ENGLISH} "Additional Windows executables that do some assistant work."
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
  !insertmacro MUI_INSTALLOPTIONS_EXTRACT "${fname_StoreEnvIni}"
  !insertmacro MUI_INSTALLOPTIONS_EXTRACT "${fname_SydoEnvIni}"

  ;Check previous installation
  ReadRegStr "$R0" ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}" "InstallTargetDir"
  ${If} "$R0" != "" ; Previous install exists
    StrCpy $INSTDIR $R0
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

  Delete "$INSTDIR\Quick start guide.url"
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\*.txt"

  Delete "$SMPROGRAMS\-GnumakeUniproc-\Uninstall.lnk"
  Delete "$SMPROGRAMS\-GnumakeUniproc-\Website.lnk"
  Delete "$SMPROGRAMS\-GnumakeUniproc-\Quick start guide.lnk"
  RMDir "$SMPROGRAMS\-GnumakeUniproc-"

  Delete "$INSTDIR\${fname_GmuEnvBat}"
  RMDir /r "$INSTDIR\GMU-main"
  RMDir /r "$INSTDIR\GMU-manual"
  RMDir /r "$INSTDIR\GMU-ext"
  RMDir /r "$INSTDIR\GMU-examples"
  RMDir /r "$INSTDIR\demo-repositories"
  RMDir /r "$INSTDIR\nsis-install"

  RMDir /r "$INSTDIR\${dirname_MinGW}"

  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}"
;  SetAutoClose true
SectionEnd

Section un.RemoveEnvVars

  DetailPrint "Removing GnumakeUniproc env-vars..."
  !insertmacro un.DelRegistryEnvVar_list ${list_GmuEnvVar}

  ; Deal with PATH env-var
  DetailPrint "Removing $\"${absdir_MinGW_bin_bkslash}$\" from PATH env-var..."
  push "${absdir_MinGW_bin_bkslash}"
  call un.RemoveFromPath

  call un.BroadcastWinIniChange

SectionEnd


;;;;;;;;;;;;;;;
Function SelectEnvVar

  ; Convert all backslash to forward-slash for $INSTDIR, then append /GMU-ext to it.
  ; We make this result the default the default value for env-ver gmu_ud_list_CUSTOM_MKI.
  Push '$INSTDIR'
  Push "\"
  Call StrSlash
  Pop $InstDir_fwslash ; StrSlash returns in $InstDir_fwslash
  !insertmacro MUI_INSTALLOPTIONS_WRITE "${fname_GmuEnvIni}" "Field 3" "State" "$InstDir_fwslash${suffix_dir_GMUext} $InstDir_fwslash${suffix_dir_ExtraCccfg}/gmu-ext"
    ; Write suggested gmp_ud_list_CUSTOM_MKI (dynamic from $InstDir).
  
  !insertmacro MUI_INSTALLOPTIONS_WRITE "${fname_GmuEnvIni}" "Field 23" "State" "$InstDir_fwslash${suffix_dir_ExtraCccfg}/compiler-cfgs"
    ; Write suggested gmp_ud_list_CUSTOM_COMPILER_CFG (dynamic from $InstDir).
  
  !insertmacro MUI_INSTALLOPTIONS_WRITE "${fname_GmuEnvIni}" "Field 12" "State" "${absdir_MinGW_bin_bkslash}"

  !insertmacro MUI_HEADER_TEXT "Select what environment variables(env-var) to set" \
    "Env-var gmu_DIR_GNUMAKEUNIPROC will be set to the dir where GnumakeUniproc.mki resides. Besides, there are more you may want to set:"
  !insertmacro MUI_INSTALLOPTIONS_DISPLAY "${fname_GmuEnvIni}"
  ; If some env-var is "checked"(for a checkbox), even with empty value, we must write its value to 
  ; Windows registry, but if some env-var is "un-checked", we must remove it from Windows registry

  ; Field 2, 3: checkbox, editbox for gmp_ud_list_CUSTOM_MKI
  !insertmacro MUI_INSTALLOPTIONS_READ $isChecked_gmp_ud_list_CUSTOM_MKI ${fname_GmuEnvIni} "Field 2" "State"
  !insertmacro MUI_INSTALLOPTIONS_READ $str_gmp_ud_list_CUSTOM_MKI ${fname_GmuEnvIni} "Field 3" "State"
  ${If} "$isChecked_gmp_ud_list_CUSTOM_MKI" == 0
    StrCpy $str_gmp_ud_list_CUSTOM_MKI ""
  ${EndIf}

  ; Field 22, 23: checkbox, editbox for gmp_ud_list_CUSTOM_COMPILER_CFG
  !insertmacro MUI_INSTALLOPTIONS_READ $isChecked_gmp_ud_list_CUSTOM_COMPILER_CFG ${fname_GmuEnvIni} "Field 22" "State"
  !insertmacro MUI_INSTALLOPTIONS_READ $str_gmp_ud_list_CUSTOM_COMPILER_CFG ${fname_GmuEnvIni} "Field 23" "State"
  ${If} "$isChecked_gmp_ud_list_CUSTOM_COMPILER_CFG" == 0
    StrCpy $str_gmp_ud_list_CUSTOM_COMPILER_CFG ""
  ${EndIf}

  !insertmacro MUI_INSTALLOPTIONS_READ $isChecked_gmp_DECO_PRJ_NAME ${fname_GmuEnvIni} "Field 6" "State"
  ${If} "$isChecked_gmp_DECO_PRJ_NAME" == 1
    StrCpy $str_gmp_DECO_PRJ_NAME 1
  ${EndIf}

  !insertmacro MUI_INSTALLOPTIONS_READ $isChecked_nlscanenv ${fname_GmuEnvIni} "Field 7" "State"

  !insertmacro MUI_INSTALLOPTIONS_READ $isChecked_gmu_LOG_OUTPUT_FILENAME ${fname_GmuEnvIni} "Field 8" "State"
  !insertmacro MUI_INSTALLOPTIONS_READ $str_gmu_LOG_OUTPUT_FILENAME ${fname_GmuEnvIni} "Field 9" "State"
  ${If} "$isChecked_gmu_LOG_OUTPUT_FILENAME" == 0
    StrCpy $str_gmu_LOG_OUTPUT_FILENAME ""
  ${EndIf}

  ; Prepare NSIS vars for gmu_DIR_ROOT, gmu_DIR_GNUMAKEUNIPROC, gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING.
  StrCpy "$isChecked_gmu_DIR_ROOT" "1"
  StrCpy "$str_gmu_DIR_ROOT" "$InstDir_fwslash"
  StrCpy "$isChecked_gmu_DIR_GNUMAKEUNIPROC" "1"
  StrCpy "$str_gmu_DIR_GNUMAKEUNIPROC" "${absdir_GmuCore}"
  StrCpy "$isChecked_gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING" "1"
  StrCpy "$str_gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING" "1"

  ${If} "$isChecked_nlscanenv" == 1
    StrCpy "$isChecked_NLSSVN" "1"
    StrCpy       "$str_NLSSVN" "https://nlssvn/svnreps"
    StrCpy "$isChecked_gv1" "1"
    StrCpy       "$str_gv1" "gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1"
    StrCpy "$isChecked_gv2" "1"
    StrCpy       "$str_gv2" "gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1"
  ${EndIf}

  !insertmacro MUI_INSTALLOPTIONS_READ $isChecked_AddPath ${fname_GmuEnvIni} "Field 11" "State"
  !insertmacro MUI_INSTALLOPTIONS_READ $str_AddPath ${fname_GmuEnvIni} "Field 12" "State"
  ; Do not clear $str_AddPath to null even if $isChecked_AddPath is 0, since it should
  ; still be set in gmuenv.bat .

  !insertmacro MUI_INSTALLOPTIONS_READ $isAddToPathFront ${fname_GmuEnvIni} "Field 13" "State"

  !insertmacro BkslashToFwslash_list ${list_GmuEnvVar}

FunctionEnd

Function StoreEnvVar

  StrCpy "$R0" "${desc_StoreEnvVar}"
  !insertmacro AppendEnvVarDef_R0_list ${list_GmuEnvVar}

  !insertmacro MUI_INSTALLOPTIONS_WRITE "${fname_StoreEnvIni}" "Field 2" "State" "$R0"

  ;Check if previous installation's saved $isStoreEnvVarToRegistry, and make it the default selection.
  ReadRegStr "$R0" ${PRODUCT_INST_ROOT_KEY} "${PRODUCT_INST_KEY}" "isStoreEnvVarToRegistry"
  ${If} "$R0" == 0
    !insertmacro MUI_INSTALLOPTIONS_WRITE "${fname_StoreEnvIni}" "Field 4" "State" 0
  ${EndIf}

  !insertmacro MUI_HEADER_TEXT "Where to store environment variables(env-var)?" ""
  !insertmacro MUI_INSTALLOPTIONS_DISPLAY "${fname_StoreEnvIni}"
  ; If "Windows registry" is "checked"(for a checkbox), set $isStoreEnvVarToRegistry to 1, otherwise 0.
  ; If "gmuenv.bat" is checked, set $isStoreEnvVarToBat to 1, otherwise 0.
  
  !insertmacro MUI_INSTALLOPTIONS_READ $isStoreEnvVarToRegistry ${fname_StoreEnvIni} "Field 4" "State"
  !insertmacro MUI_INSTALLOPTIONS_READ $isStoreEnvVarToBat ${fname_StoreEnvIni} "Field 5" "State"

  ${If} "$MUI_TEMP1" == "back"
  ${OrIf} "$MUI_TEMP1" == "cancel"
  ${OrIf} "$MUI_TEMP1" == "error"
    Return
  ${EndIf}

  ${If} "$isStoreEnvVarToBat" == 1
    Delete ${fpath_GmuEnvBat} ; may try /REBOOTOK
  ${EndIf}
  ; note: $isStoreEnvVarToRegistry is processed elsewhere(in -AddEnvVars)

FunctionEnd

Function LaunchQuickStartGuide
  ExecShell "" "${fpath_QuickStartGuide}"
FunctionEnd
