# NOTE: You MUST `source' this script(should let current env modified) instead of executing it.

# _gmu_rel2abs (): 
# Input a dir(relative or absolute), return(echo) its absolute dir.
# If the input dir is not valid or not accessible, return null string.
# This function will not change callers current working directory.
_gmu_rel2abs ()
{
	if [ "$1" = "" ]; then return 4; fi

	if cd $1 >/dev/null; then echo $(pwd)
	else return 5; fi
}

if [ "$1" != "" ]; then
	_gmu_root="$1"
	# Note: $1 must be an absolute dir(start with /) and not end with / .
	# An example would be:
	#	/home/chj/GMU
else
	# USER NOTE: ${BASH_SOURCE} (used below) is only supported on Bash 3.0 and above,
	# so, for Bash 2.0 and prior, user must provide $1, otherwise, wrong result will arise.
	_gmu_root="${BASH_SOURCE%/*}"
	_gmu_root=$(_gmu_rel2abs "$_gmu_root")
	if [ "$_gmu_root" = "" ]; then 
		echo "Error! Cannot deduce your GMU root dir. Please assign a GMU root dir manually."
		return 4
	fi
	_gmu_root="${_gmu_root%/*}" # another level of parent dir
fi
# Note: I redirect cd's stdout output to /dev/null because some user
# may define cd as an alias and output something.
#	[2007-03-03]But I think it's better to deduce _gmu_root from
# where this file resides. I could have done that if I knew how to get the
# full path of the file being sourced inside the very being sourced file.

echo "From set-gmuenv.sc: export env-var:"
echo "    gmu_DIR_ROOT=$_gmu_root"
echo "    gmu_DIR_GNUMAKEUNIPROC=$_gmu_root/GMU-main/GnumakeUniproc"

export gmu_DIR_ROOT=$_gmu_root
export gmu_DIR_GNUMAKEUNIPROC=$gmu_DIR_ROOT/GMU-main/GnumakeUniproc

if [ ! -f "$gmu_DIR_GNUMAKEUNIPROC/GnumakeUniproc.mki" ]; then
	echo "Error! The file \"$gmu_DIR_GNUMAKEUNIPROC/GnumakeUniproc.mki\" does not exist,\
 you may have given a wrong dir as the parameter or GnumakeUniproc.mki is missing."
	return 1
fi

# Check if make-gmu can be executed. If so, let umake use it(by overriding gmu_MAKE_EXE)
if $gmu_DIR_ROOT/bin/make-gmu --version > /dev/null; then
	export gmu_MAKE_EXE=make-gmu
fi

export gmu_LOG_OUTPUT_FILENAME=_gmulog.txt #Set to null if you don't want to log make output

export gmp_ud_list_CUSTOM_MKI=$gmu_DIR_ROOT/GMU-ext
# export gmp_PS_INCLUDE_SUBDIRS=linux // the old one
export gmp_DECO_PRJ_NAME=1

PATH="$gmu_DIR_ROOT/bin:$PATH"

echo    "Success! To see all gmu-vars set into env, type command:   set | grep -e \"^gm[a-z]_\""

_gmu_root=
