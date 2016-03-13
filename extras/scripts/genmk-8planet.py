#!/usr/bin/env python

"""
Generate a makefile that is capable to build 8-variant GMU subprjs.
Suitable for Visual C++ compiler.

Cconf  Debug/Release  Unicode/MBCS  LIB/DLL  Naming  
RML    Release        MBCS          LIB      name.lib  
RMD    Release        MBCS          DLL      name--imp.lib , name.dll  
RUL    Release        Unicode       LIB      name_U.lib  
RUD    Release        Unicode       DLL      name_U--imp.lib , name_U.dll  
DML    Debug          MBCS          LIB      name_D.lib  
DMD    Debug          MBCS          DLL      name--imp.lib , name.dll  
DUL    Debug          Unicode       LIB      name_U_D.lib  
DUD    Debug          Unicode       DLL      name_U--imp.lib , name_U.dll  

Options for running this .py:
--prjname=<prjname>
--libmakefile=<makefile-path>
--dllmakefile=<makefile-path>

--output-file=<makefile>

Options for running the generated makefile:

gmb_planets=<build-variant-list>

Example:
   gmb_planets="RML RUL"
   
   Build two variants: Release/MBCS/lib and  Release/Unicode/lib .
   or, ``gmb_planets=all'', build all 8 variants.
   or, ``gmb_planets=alluc'', build all 4 Unicode variants.
   or, ``gmb_planets=allmb'', build all 4 MBCS variants.
   
gmb_syncto=<root-dir>

Example:
	gmb_syncto=D:/SDKOutput
	
	Copy the generated headers,libs,dlls to D:/SDKOutput directory.

gmb_bintray=<dirname>

Example:
	bintray=vc8
	
	LIBs will be copied to D:/SDKOutput/vc8/lib
	DLLs will be copied to D:/SDKOutput/vc8/bin-debug or D:/SDKOutput/vc8/bin-debug .

	See NlsWiki pageId=47907618 for directory layout spec for the bintray thing.


gmb_ : GnuMake Script assistant.
"""

import sys
import getopt
import re
import os

version = "1.2"

libmakefile = ""
dllmakefile = ""
fMakefile = "" # Output makefile

opts = {}

def MakeBodyText1V(idx, isDebug, isUnicode, isDll):
	if isDll and not dllmakefile: return ''
	if (not isDll) and (not libmakefile): return ''
	refname = ''
	refname += 'D' if isDebug else 'R'
	refname += 'U' if isUnicode else 'M'
	refname += 'D' if isDll else 'L'
	pattern = """
ifeq ($(findstring %(refname)s,$(gmb_planets)),%(refname)s) #if $(gmb_planets) contains %(refname)s
# [%(idx)d] %(refname)s: %(sDorR)s , %(sUnicode)s, %(sDLL)s
gmu_uv_list_ALL_SUBPRJ+=%(refname)s
%(refname)s_Makefile:=%(subprjmkf)s
%(refname)s_MakeVarDefines:=gmp_bc_DEBUG=%(bDebug)s gmp_bc_UNICODE=%(bUnicode)s \\
  gmp_u_list_PLUGIN_TO_LOAD_AUX_PRE="PI_sync_devoutput PI_sync_debug_info"\\
  gmi_SYDO_SHOW_COPY_CMD=1 gmp_msvc_WANT_RELEASE_PDB=1 \\
  gmi_SYDO_ud_SYNC_HEADER_TO=$(gmb_syncto)/include \\
  gmi_SYDO_ud_SYNC_LIB_TO=$(gmb_syncto)/$(gmb_bintray)/lib \\
  gmi_SYDO_ud_SYNC_DLL_TO=$(gmb_syncto)/$(gmb_bintray)/bin-%(sDorR)s \\
  gmi_SYDO_ud_SYNC_DBGINFO_TO=$(gmb_syncto)/$(gmb_bintray)/%(sdDbgInfo)s
%(refname)s_IsForcePostProc:=1
endif
"""	
	bDebug = "1" if isDebug else ""
	bUnicode = "1" if isUnicode else ""
	sDorR = "debug" if isDebug else "release"
	sdDbgInfo = ("bin-"+sDorR) if isDll else "lib"
	sret = pattern % {
		"idx" : idx+1,
		"refname" : refname,
		"subprjmkf" : dllmakefile if isDll else libmakefile,
		"bDebug" : bDebug,
		"bUnicode" : bUnicode,
		"sDorR" : sDorR,
		"sdDbgInfo" : sdDbgInfo,
		"sUnicode" : "Unicode" if isUnicode else "not-Unicode",
		"sDLL" : "DLL" if isDll else "LIB",
	}
	return sret

def MakeBodyText(prjname):
	makefile_content = """
# Don't hand edit this makefile. It is generated by genmk-8planet.py .
# And don't check in this file into source control system.
include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-concise-header.mki
gmu_PRJ_NAME=%(prjname)s-1c
ifeq (1,$(_isNowNotGmuGetPrjAttr))
#### >>>>

ifndef gmb_planets
  $(error gmb_planets is not defined)
endif
ifndef gmb_syncto
  $(error gmb_syncto is not defined)
endif
ifndef gmb_bintray
  $(error gmb_bintray is not defined)
endif
ifeq ($(strip $(gmb_planets)),all)
  override gmb_planets=RML RMD RUL RUD DML DMD DUL DUD
else ifeq ($(strip $(gmb_planets)),alluc)
  override gmb_planets=RUL RUD DUL DUD
else ifeq ($(strip $(gmb_planets)),allac)
  override gmb_planets=RML RMD DML DMD
endif
%(chunks_subprjinfo)s

#### <<<<
endif # ifeq (1,$(_isNowNotGmuGetPrjAttr))
include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-container.mks
"""
	chunks_subprjinfo = ''
	idx = 0
	for isDebug in [False, True]:
		for isUnicode in [False, True]:
			for isDll in [True, False]:
				chunks_subprjinfo += MakeBodyText1V(idx, isDebug, isUnicode, isDll)
				idx+=1

	sret = makefile_content % { 'prjname':prjname , 'chunks_subprjinfo':chunks_subprjinfo }
	return sret

def main():
	global opts, libmakefile, dllmakefile, fMakefile;
	
	optlist,arglist = getopt.getopt(sys.argv[1:], '', 
		['prjname=', 'libmakefile=', 'dllmakefile=', 'output-file=', 'version'])
	opts = dict(optlist)

	if '--version' in opts:
		print 'genmk-8planet.py v%s'%(version)
		return 0;
	
	if '--output-file' in opts:
		fMakefile = opts['--output-file']
	else:
		print 'No input file! You have to assign a output makefile filename.'
		return 1;

	if not ( ('--libmakefile' in opts) or ('--dllmakefile' in opts) ):
		print 'Neither --libmakefile nor --dllmakefile is assigned. I can do nothing!'
		return 2;

	if '--libmakefile' in opts:
		libmakefile = opts['--libmakefile']
	
	if '--dllmakefile' in opts:
		dllmakefile = opts['--dllmakefile']
		
	if '--prjname' in opts:
		prjname = opts['--prjname']
	else:
		print 'Error: --prjname is not assigned.'
		return 4

	content = MakeBodyText(prjname)

	fhMakefile = open(fMakefile, 'w')
	fhMakefile.write(content)
	fhMakefile.close()
	
	return 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
