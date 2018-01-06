# NOTE: You MUST `source' this script(should let current env modified) instead of executing it.

if [ "$gmu_DIR_ROOT" = "" ]; then
	echo "ERROR from _gmuenv.sc: Env-var gmu_DIR_ROOT not defined yet."
	return 4
fi

export gmu_DIR_GNUMAKEUNIPROC=$gmu_DIR_ROOT/GMU-main/GnumakeUniproc

if [ ! -f "$gmu_DIR_GNUMAKEUNIPROC/GnumakeUniproc.mki" ]; then
	echo "Error! The file \"$gmu_DIR_GNUMAKEUNIPROC/GnumakeUniproc.mki\" does not exist,\
 you may have given a wrong dir as the parameter or GnumakeUniproc.mki is missing."
	return 1
fi

# Check if gmu-make can be executed. If so, let umake use it(by overriding gmu_MAKE_EXE)
if $gmu_DIR_ROOT/GMU-main/umake_cmd/bashcmd/gmu-make --version > /dev/null; then
	export gmu_MAKE_EXE=gmu-make
fi

# [2009-12-19] GNU make uses /bin/sh as default command shell, and GMU requires 
# Bourne shell or Bash.
# so here we check whether /bin/bin really is Bourne shell or Bash. If not, 
# we force GMU to use /bin/bash by setting gmu-var gmu_FORCE_BASH_PATH(if it is not set yet).
# 
# Case: On Ubuntu 9.10, /bin/sh defaults to /bin/dash, and dash's builtin command echo does not  
# recognize "-e" as an option and "-e" is sent to stdout literally, so we can test it.
if [ "$gmu_FORCE_BASH_PATH" = "" ]; then
  toutput=`/bin/sh -c "echo -e ABC"`
  if [ "$toutput" != "ABC" ]; then export gmu_FORCE_BASH_PATH="/bin/bash"; fi
fi

export gmu_ver=0.105

export gmp_ud_list_CUSTOM_MKI="$gmp_ud_list_CUSTOM_MKI $gmu_DIR_ROOT/GMU-ext $gmu_DIR_ROOT/nlscan/gmu-ext"
export gmp_ud_list_CUSTOM_COMPILER_CFG="$gmp_ud_list_CUSTOM_COMPILER_CFG $gmu_DIR_ROOT/nlscan/compiler-cfgs"

export gmp_DECO_PRJ_NAME=1

[ "$gmu_LOG_OUTPUT_FILENAME" = "" ] && export gmu_LOG_OUTPUT_FILENAME=_gmulog.txt

export gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING=1


export _gmuex1=$gmu_DIR_ROOT/GMU-examples/common/walkdir/make-all
export gv1="gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1"
export gv2="gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1"


if [ "$gmp_COMPILER_ID" = "" ]; then
  export gmp_COMPILER_ID=linuxgcc
	# Note: Disable this only in case you use other compiler than gcc(linux targeted).
fi

PATH="$gmu_DIR_ROOT/GMU-main/umake_cmd/bashcmd:$PATH"

# Something extra for Nlscan and Scalacon:
export NLSSVN=https://nlssvn/svnreps
#export gmp_NO_LoadCenv_linuxgcc_gcc45_i586=1
	# For compiler-env of linuxgcc,gcc45_i586 pair
#export gmp_NO_LoadCenv_linuxgcc_gcc45_x64=1
	# For compiler-env of linuxgcc,gcc45_x64 pair
	
