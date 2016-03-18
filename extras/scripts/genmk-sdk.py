#!/usr/bin/env python

"""
This is called by GMU PI_makesdk_2016 plugin.
"""

import sys
import getopt
import re
import os
import ConfigParser

version = "1.2"

opts = {}
prjname = ''
gmb_syncto = ''
fConfig = '' # the config file(in INI format)
IniInfo = {} #This records static info extracted from buildsdk.ini
g_compiler_ids = [] # from compiler-id section names in the INI, with 'compiler-id.' prefix removed.
	# Sample: ['msvc', 'wince']

def IniAssertKeyExist(section, key):
	"""
	For IniInfo, check #key exist(non-null) in #section. Assert error and exit if not.
	"""
	if not key in IniInfo[section]:
		print 'Error in %s: key "%s" missing from section [%s].'%(fConfig, key, section)
		exit(4)

def IniSetKeyDefault(section, key, default=''):
	"""
	For IniInfo, check #key exist(non-null) in #section.
	If that key does not exist, set its value to #default .
	"""
	if not key in IniInfo[section]:
		IniInfo[section][key] = default


def cid_section_name(cid):
	return 'compiler-id.'+cid

def get_fname_cenv_mki(compiler_id, compiler_ver):
	return 'cenv-%s-%s.mki'%(compiler_id,compiler_ver)

def makefile_1c_getname(compiler_id):
	return '__Makefile-'+compiler_id+'-1c'

def GenOneUxm_in_vbuxm(idx, section_name, dsection):
	chunk_uxm = r"""
##################################################################################################
# User example [%(idx_show)d-%(vidx_show)d] umkvariant=%(umkvariant)s : %(dirSdkOut)s/%(examples_copyto)s/%(f_Makefile)s
##################################################################################################
  tmp_subprj_cver := %(compiler_ver)s
  tmp_isCidverMatch := $(call gmuf_IsWordInSet,%(compiler_id)s$(_GmuComma)$(tmp_subprj_cver),$(_list_cidcver_used))
  tmp_CidMatchAnyCver := $(if $(tmp_subprj_cver),,$(call gmuf_pick_one_cver_by_cid,%(compiler_id)s,$(_list_cidcver_used)))
  ifneq (,$(tmp_CidMatchAnyCver))
    # assign a compiler-ver to this subprj, otherwise, we cannot know what cenv-<cid>-<cver>.mki to load.
    tmp_subprj_cver := $(tmp_CidMatchAnyCver)
    $(info Scalacon info: Auto-selecting compiler-ver ``$(tmp_subprj_cver)'' for example-section [%(section_name)s] umkvariant=%(umkvariant)s)
  endif
  ifneq (,$(tmp_isCidverMatch)$(tmp_CidMatchAnyCver))
    fname_cenv_mki := cenv-%(compiler_id)s-$(tmp_subprj_cver).mki
    tmp_cenvmki := $(firstword $(wildcard $(patsubst %%,%%/compiler-env/$(fname_cenv_mki),$(gmp_ud_list_CUSTOM_COMPILER_CFG) $(gmu_DIR_GNUMAKEUNIPROC)/pattern1cfg)))
    ifeq (,$(tmp_cenvmki))
      ifndef gmp_NO_LoadCenv_%(compiler_id)s_$(tmp_subprj_cver)
        $(error For compiler-id,compiler-ver pair ``%(compiler_id)s,$(tmp_subprj_cver)'', no $(fname_cenv_mki) file can be found in $$(gmp_ud_list_CUSTOM_COMPILER_CFG)/compiler-env or $$(gmu_DIR_GNUMAKEUNIPROC)/pattern1cfg/compiler-env)
      endif
    else
      include $(tmp_cenvmki)
    endif
    
    %(uxm_cidver_var)s := $(tmp_subprj_cver)
    	# Define a unique make-var so that it's value can be retreived when %(refname)s_MakeVarDefines is delay-expanded. 
    	# ( $(tmp_subprj_cver) itself will be overwritten across multiple uxm makefile chunks)
    	# So, $(%(uxm_cidver_var)s) will be sth like "vc80" , "vc100x64" etc
    gmu_uv_list_ALL_SUBPRJ += %(refname)s
    %(refname)s_Makefile = %(dirSdkOut)s/%(examples_copyto)s/%(f_Makefile)s
    %(refname)s_MakeVarDefines = \
      gmp_COMPILER_ID=%(compiler_id)s gmp_COMPILER_VER_%(compiler_id)s=$(%(uxm_cidver_var)s) \
      %(ud_makevars)s \
      gmp_u_list_PLUGIN_TO_LOAD_ENV_PRE="PI_sync_devoutput PI_sync_debug_info"\
      gmi_SYDO_ud_SYNC_EXE_TO=$(absdir_example_bins)/$(%(uxm_cidver_var)s)\
      gmi_SYDO_ud_SYNC_DBGINFO_TO=$(absdir_example_bins)/$(%(uxm_cidver_var)s)\
      $(gmpf_LoadCenv_%(compiler_id)s_$(%(uxm_cidver_var)s))

    %(uxm_dirbin_var)s := $(absdir_example_bins)/$(%(uxm_cidver_var)s)
    
    ifneq (,$(strip %(copydlls)s))
      gmp_USER_POST_TARGETS += COPYDLLS_%(refname)s
    endif
    ifeq (1,$(call gmuf_IsWordInSet,$(%(uxm_cidver_var)s),$(gmb_run_example_on_compiler_vers)))
    ifeq (run1,run$(strip %(isrunverify)s))
      gmp_USER_POST_TARGETS += RUN_%(refname)s
      cmd_%(refname)s := %(runcmd)s
    endif
    endif
  else
    $(info Scalacon info: Example-makefile "%(dirSdkOut)s/%(examples_copyto)s/%(f_Makefile)s" is skipped for umkvariant(%(umkvariant)s) because you did not tell GMU to build its libraries.)
  endif # Check $(_list_cidcver_used) to filter out "not-used [cid,cver]"
#
.PHONY: COPYDLLS_%(refname)s
COPYDLLS_%(refname)s:
	@$(if %(uxm_is_copy_selfdll)s,echo "Copying DLLs from $(gmb_syncto)/$(%(uxm_cidver_var)s)/%(uxm_copy_binvariant)s"; $(CP_preserve_time) --force $(gmb_syncto)/$(%(uxm_cidver_var)s)/%(uxm_copy_binvariant)s/* $(%(uxm_dirbin_var)s))
#
.PHONY: RUN_%(refname)s
RUN_%(refname)s:
	@echo "Verify-run example for [%(section_name)s](umkvariant=%(umkvariant)s):"
	@echo ">Working-directory:"
	@echo ">   $(%(uxm_dirbin_var)s)"
	@echo ">Shell command-line:"
	@echo ">   $(call _TrShcmd4echo,$(subst %%{exename},$(call gmuf_GetSubprjOutputNameByRefname,%(refname)s),$(cmd_%(refname)s)))"
	@cd "$(%(uxm_dirbin_var)s)";\
		$(subst %%{exename},$(call gmuf_GetSubprjOutputNameByRefname,%(refname)s),$(cmd_%(refname)s))
	@echo "Verify-run exit-code is 0, success."

"""
	retstr = ''
	
	dirSdkOut = gmb_syncto
	examples_copyto = IniInfo['global']['examples_copyto']

	f_Makefile = dsection['umk']
	
	umkvariants = dsection['umkvariants']
	umkvlist = umkvariants.split() # was CRLF separated

	for vidx, umkvariant in enumerate(umkvlist):
		# umkvariant is like "msvc,vc80,ud" etc, the final part ",ud " may be omitted
		
		umkv_parts = umkvariant.split(',')
		compiler_id = umkv_parts[0]
		if not compiler_id in g_compiler_ids:
			continue # If .bin of this compiler_id is not built, neither should its examples be built. (possibly no compiler installed for it)
		
		compiler_ver = umkv_parts[1] if len(umkv_parts)>1 else ''
		ud = umkv_parts[2] if len(umkv_parts)>2 else ''
		ud_makevars = ''
		ud_makevars += 'gmp_bc_UNICODE=%s '%('1' if ('u' in ud) else '')
		ud_makevars += 'gmp_bc_DEBUG=%s '%('1' if ('d' in ud) else '')

		copydlls = dsection['copydlls'].strip() if 'copydlls' in dsection else ''
			# a space separated string, like "self sdkin1 sdkin2" .
			# "self" is reserved word meaning all things in $/sdkout (i.e. self)
			# (not implemented yet): sdkin1, sdkin2 are placeholders for other dll's name, no need to add _U or .dll suffix here.
		isrunverify = dsection['isrunverify'].strip() if 'isrunverify' in dsection else ''
		runcmd = dsection['runcmd'] if 'runcmd' in dsection else ''

		idx_show = idx+1
		vidx_show = vidx+1
		uxm_dirbin_var = "uxm_%d_%d_dirbin"%(idx_show, vidx_show) # the GNU make var-name will be sth like uxm_1_2_dirbin
		uxm_cidver_var = "uxm_%d_%d_cidver"%(idx_show, vidx_show) # the GNU make var-name will be sth like uxm_1_2_cidver
		
		uxm_is_copy_selfdll = '1' if 'self' in copydlls.split() else ''
		uxm_copy_binvariant = 'bin-release' # because example-bin does not fork into bin-debug//bin-release, so I just use bin-release.
		# // uxm_copy_binvariant = 'bin-debug' if ('d' in ud) else 'bin-release'
		
		refname = 'uxmRefname_%s_%s_'%(idx_show,vidx_show) + umkvariant.replace(',','_')
			# use idx and vidx in GMU subprj refname to avoid refname conflict

		retstr += chunk_uxm % locals()
	
	return retstr


def GenMakefile_vbuxm(prjname):
	makefile_content = """
# Don't hand edit this makefile. It is generated by genmk-sdk.py .
# And don't check in this file into source control system.
include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-concise-header.mki
gmu_PRJ_NAME=%(prjname)s-vbuxm
gmu_ALLOW_ZERO_SUBPRJ=1
	# If user builds the SDK with partial compilers, subprjs may be empty, so define this to suppress no-subprj error.

ifeq (,$(strip $(gmb_example_bin_dirname)))
  gmb_example_bin_dirname := example-bin
endif
absdir_example_bins := $(gmb_syncto)/$(gmb_example_bin_dirname)

ifeq ($(_isNowNotGmuGetPrjAttr),1) # No need to include the big chunks below when doing _gmu_ut_GetPrjAttr
_list_cidcver_used := $(shell cat _cidcver_used.gmu.txt)
%(chunks_subprjuxm)s
endif # ifeq ($(_isNowNotGmuGetPrjAttr),1)

include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-container.mks
"""
	chunks_subprjuxm = ''
	idx = 0
	for section_name in IniInfo:
		prefix = 'example.'
		if not section_name.startswith(prefix):
			continue
		
		dsection = IniInfo[section_name] # d implies python dict
		# Check that there is required keys in this section.
		if (not 'umk' in dsection) or (dsection['umk'].strip()==''):
			print 'Scalacon Error: Section [%s] in your INI file "%s" does not have a "umk" key.'%(
				section_name, fConfig)
			exit(6)
		
		if (not 'umkvariants' in dsection) or (dsection['umkvariants'].strip()==''):
			print 'Scalacon Error: Section [%s] in your INI file "%s" does not have a "umkvariants" key.'%(
				section_name, fConfig)

		chunks_subprjuxm += GenOneUxm_in_vbuxm(idx, section_name, dsection)
		idx += 1
	
	if not chunks_subprjuxm: 
		# No user examples assigned in INI(no GMU subprj), so write this line to avoid GMU make error.
		chunks_subprjuxm = 'gmu_DELIBERATE_NO_SUBPRJ=1\n'
	
	str_write = makefile_content%locals()
	open('__Makefile-vbuxm', 'w').write(str_write)
	

def GenMakefile_cpuxm(prjname, copyto, f_buildsdk_ini):
	"""
	Generate a GMU free-style makefile that copies tree content in #copyfrom to #copyto.
	If directory #copyto does not exist yet, we'll create it.
	@#copyfrom is from f_buildsdk_ini -> [global] -> examples_dir
	"""
	makefile_content = """
# Don't hand edit this makefile. It is generated by genmk-sdk.py .
# And don't check in this file into source control system.
include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-concise-header.mki
gmu_PRJ_NAME=%(prjname)s-cpuxm
gmu_FREE_STYLE_MAKEFILE=1
gmp_USER_FREE_STYLE_TARGET=cpuxm
pycmd:=genmk-sdk-cpuxm.py --gmb_syncto=%(copyto)s %(f_buildsdk_ini)s
.PHONY: cpuxm
cpuxm:
	@echo '$(pycmd)'
	@$(call gmuf_ScriptCmd,$(pycmd))
include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-container.mks
""" % locals()
	fh = open('__Makefile-cpuxm', 'w')
	fh.write(makefile_content)
	fh.close()


def GenOneSubprj_in_mc(idx, compiler_id, cidver, bintray, planets_cid, planets_cidver=''):
	refname = 'subprjRefname_' + compiler_id + '_' + cidver
	Makefile_1c = makefile_1c_getname(compiler_id)
	fname_cenv_mki = get_fname_cenv_mki(compiler_id, cidver)
	chunk_subprj = """
  # [%(idx)d] %(compiler_id)s, %(cidver)s
  ifeq (1,$(call gmuf_IsWordInWords,%(compiler_id)s,$(gmb_compiler_ids)))
  ifeq (1,$(call gmuf_IsWordInWords,%(cidver)s,$(gmb_%(compiler_id)s_vers)))
    tmp_cenvmki := $(firstword $(wildcard $(patsubst %%,%%/compiler-env/%(fname_cenv_mki)s,$(gmp_ud_list_CUSTOM_COMPILER_CFG) $(gmu_DIR_GNUMAKEUNIPROC)/pattern1cfg)))
      # find the first cenv-<cid>-<ver>.mki file which contains the compiler-env-vars
    ifeq (,$(tmp_cenvmki))
      ifndef gmp_NO_LoadCenv_%(compiler_id)s_%(cidver)s
        $(error For compiler-id,compiler-ver pair ``%(compiler_id)s,%(cidver)s'', no %(fname_cenv_mki)s file can be found in $$(gmp_ud_list_CUSTOM_COMPILER_CFG)/compiler-env or $$(gmu_DIR_GNUMAKEUNIPROC)/pattern1cfg/compiler-env)
      endif
    else
      include $(tmp_cenvmki)
    endif
    gmu_uv_list_ALL_SUBPRJ += %(refname)s
    %(refname)s_Makefile := %(Makefile_1c)s
    %(refname)s_MakeVarDefines := gmp_COMPILER_ID=%(compiler_id)s gmp_COMPILER_VER_%(compiler_id)s=%(cidver)s \\
      gmb_planets=$(call _get_specific_gmb_planets,%(compiler_id)s,%(cidver)s,%(planets_cid)s,%(planets_cidver)s) \\
      gmb_bintray=%(bintray)s $(gmpf_LoadCenv_%(compiler_id)s_%(cidver)s)
    $(shell echo "%(compiler_id)s,%(cidver)s" >> _cidcver_used.gmu.txt)
  endif
  endif
""" % locals()
	return chunk_subprj


def GenMakefiles(prjname):
	"""
	Generate makefiles from IniInfo.
	"""
	mkfMc_content = """
# Don't hand edit this makefile. It is generated by genmk-sdk.py .
# And don't check in this file into source control system.
include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-concise-header.mki
gmu_PRJ_NAME=%(prjname)s-mc
gmp_COMPILER_ID=
ifeq (1,$(_isNowNotGmuGetPrjAttr))
#### >>>>

ifndef gmb_syncto
  $(error gmb_syncto is not defined)
endif
_get_specific_gmb_planets = $(strip $(if $(gmb_planets_$1_$2),$(gmb_planets_$1_$2),$(if $4,$4,\\
  $(if $(gmb_planets_$1),$(gmb_planets_$1),$3))))
	# $1: compiler-id , $2: compiler-ver , $3: planets of current $1 from ini , $4: planets of current $1.$2 from ini
	# $4 may be null to indicate no such assignment in ini; $3 must not be null, at least "all" should be given
	# Get gmb_planets value for subprj, from more specific assignment to less specific assignment.
ifeq (,$(strip $(gmb_compiler_ids)))
  override gmb_compiler_ids=%(compiler_ids_str)s
endif
gmu_up_list_STARTUP_CLEAR_FILES+=_cidcver_used.gmu.txt# This records what compiler-id,compiler-ver is used in this make-sdk run.
%(chunks_ini_compiler_vers)s
%(chunks_subprjinfo)s
ifeq (,$(strip $(gmu_uv_list_ALL_SUBPRJ)))
  $(error You don't assign any valid value to any of the following $(words $(gmb_compiler_ids)) var(s): $(foreach c,$(gmb_compiler_ids),gmb_$c_vers), so I don't know what to build)
endif

#### <<<<
endif # ifeq (1,$(_isNowNotGmuGetPrjAttr))
include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-container.mks
"""
	assert g_compiler_ids # it's a list 
	compiler_ids_str = ' '.join(g_compiler_ids)

	pattern_cver = """
ifeq (,$(strip $(gmb_%(cid)s_vers)))
  override gmb_%(cid)s_vers=%(cur_vers)s
endif
"""
	chunks_ini_compiler_vers = ''
	for cid in g_compiler_ids:
		cur_vers = IniInfo[cid_section_name(cid)]['cidvers']
		chunks_ini_compiler_vers += pattern_cver % locals()

	chunks_subprjinfo = ''
	idx = 0
	# For every compiler-id,compiler-ver pair, generate a chunk of makefile statement corresponding to a make subprj.
	for cid in g_compiler_ids:
		cid_info = IniInfo[cid_section_name(cid)]
		# memo: Each cid_info corresponds to one [compiler-id.xxx] section.
		# cid_info['inikey'] gets an inikey's value from this INI section.

		# Generate per-subprj chunk for __Makefile-mc (chunks_subprjinfo)
		cidvers = cid_info['cidvers']
		for cidver in cidvers.split():
			# cidver may be 'vc60', 'vc80x64' etc
			bintray = cid_info['bintray'].replace('%{cidver}', cidver)

			# Process planets.<cidver> for this cid
			planets_cidver = cid_info['planets.'+cidver] if ('planets.'+cidver in cid_info) else ''

			idx += 1
			sret = GenOneSubprj_in_mc(idx, cid, cidver, bintray, cid_info['planets'], planets_cidver)
			chunks_subprjinfo += sret

		# Generate __Makefile-<cid>-1c files, using another .py

		cmd_genmk_8planet = "genmk-8planet.py --prjname=%s"%(prjname)
		libmakefile = cid_info['libmakefile']
		dllmakefile = cid_info['dllmakefile']
		if libmakefile: 
			cmd_genmk_8planet += ' --libmakefile=%s'%(libmakefile)
		if dllmakefile: 
			cmd_genmk_8planet += ' --dllmakefile=%s'%(dllmakefile)
		cmd_genmk_8planet += ' --output-file=__Makefile-'+cid+'-1c'

		# zzz: why using popen()?
		fh1c = os.popen(cmd_genmk_8planet) # This generates u_subprjs-msvc-1c.mki(zzz: wrong comment?)
		strret = fh1c.readlines()
		exitcode = fh1c.close()
		if exitcode:
			print 'Error executing: %s'%(cmd_genmk_8planet)
			exit(5)
		# Q: how to close fh1c here?


	# We can generate __Makefile-mc now.
	mkfMc_content = mkfMc_content % locals()
	fhmc = open('__Makefile-mc', 'w')
	fhmc.write(mkfMc_content)
	fhmc.close()

	if IniInfo['global']['examples_dir']:
		GenMakefile_cpuxm(prjname, gmb_syncto, fConfig) # generate file __Makefile-cpuxm

		# Prepare makefile statement for building user examples in their SDK output dir.
		GenMakefile_vbuxm(prjname) # generate file __Makefile-vbuxm


def ExtractIniInfo(iniobj):
	"""
	iniobj is a ConfigParser object
	This function outputs info in IniInfo.

	This function turn IniInfo into an easy using facility, i.e. let IniInfo can be used in form of
	value = IniInfo['some-section']['key-in-that-section']
	"""
	global IniInfo

	all_sections = iniobj.sections()
	for section in all_sections:
		IniInfo[section] = {}
		kvpairs = iniobj.items(section)
		for key, value in kvpairs:
			IniInfo[section][key] = value

	## Check missing or invalid key-value pairs

	# Check the 'global' section
	IniSetKeyDefault('global', 'examples_dir')
	if IniInfo['global']['examples_dir']:
		if not 'examples_copyto' in IniInfo['global']:
			print 'Scalacon Error: In "%s", you assign values for example_dir, but does not assign examples_copyto yet.'%(fConfig)
			exit(3)

	# Check every "compiler-id." section, and set defaults for them
	# [compiler-id.msvc], [compiler-id.wince] etc
	for section in IniInfo:
		if not section.startswith('compiler-id.'): 
			continue

		g_compiler_ids.append(section.replace('compiler-id.', ''))
		cid = section
		IniAssertKeyExist(cid, 'cidvers')
		IniSetKeyDefault(cid, 'libmakefile')
		IniSetKeyDefault(cid, 'dllmakefile')

		if (not IniInfo[cid]['libmakefile']) and (not IniInfo[cid]['dllmakefile']):
			print 'Scalacon Error: Neither libmakefile or dllmakefile is assigned in section [%s]'%(cid)
			exit(4)

		IniSetKeyDefault(cid, 'planets', 'all')
		IniSetKeyDefault(cid, 'bintray', '%{cidver}')
	
	if not g_compiler_ids:
		print 'Scalacon Error: Your INI file does not have any [compiler-id.xxx] section.'
		exit(2)


def main():
	global opts, prjname, gmb_syncto, fConfig;

	optlist,arglist = getopt.getopt(sys.argv[1:], '', ['prjname=', 'gmb_syncto=', 'version'])
	opts = dict(optlist)

	if '--version' in opts:
		print '%s v%s'%(os.path.basename(__file__), version)
		return 0;

	if(len(arglist)==0):
		print 'No input file! This program requires an INI file input.'
		return 1;

	if '--prjname' in opts:
		prjname = opts['--prjname']
	else:
		print 'No --prjname=<prjname> given. I cannot continue.'
		return 1

	if '--gmb_syncto' in opts:
		gmb_syncto = opts['--gmb_syncto']
	else:
		print 'No --gmb_syncto=<SDKoutput-dir> given. I cannot continue.'
		return 1

	fConfig = arglist[0]

	# Open config file(INI)
	config = ConfigParser.ConfigParser()
	try:
		readret = config.read(fConfig)
	except(MissingSectionHeaderError):
		print "Error: %s seem not to be a valid configuration file."%(fConfig)
		return 2

	if not readret:
		print 'Error: The config file %s does not exist or cannot be opened.'%(fConfig)
		return 3

	ExtractIniInfo(config)
	GenMakefiles(prjname)

	return 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
