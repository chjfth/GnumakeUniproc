
if [ "$1" != "" ]; then
	_gmu_root="$1"; 
	# Note: $1 must be an absolute dir(start with /) and not end with / .
	# An example would be:
	#	/home/chj/GMU
else
	_gmu_root="`(cd .. > /dev/null; pwd)`";
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
	echo "Warning! The file \"$gmu_DIR_GNUMAKEUNIPROC/GnumakeUniproc.mki\" does not exist,\
 you may have given a wrong dir as the parameter or GnumakeUniproc.mki is missing."
fi

export gmu_LOG_OUTPUT_FILENAME=_gmulog.txt #Set to null if you don't want to log make output

export gmp_ud_list_CUSTOM_MKI=$gmu_DIR_ROOT/GMU-ext
# export gmp_PS_INCLUDE_SUBDIRS=linux // the old one
export gmp_DECO_PRJ_NAME=1

echo    "To see all gmu-vars set into env, type command:   set | grep -e \"^gm[a-z]_\""

_gmu_root=
