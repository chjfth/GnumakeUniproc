
export gmu_DIR_ROOT=$(\cd `dirname ${BASH_SOURCE}` && pwd)

source $gmu_DIR_ROOT/_gmuenv.sc

if [ ! -f "$gmu_DIR_GNUMAKEUNIPROC/GnumakeUniproc.mki" ]; then
	echo "Error! The file \"$gmu_DIR_GNUMAKEUNIPROC/GnumakeUniproc.mki\" does not exist,\
 you may have given a wrong dir as the parameter or GnumakeUniproc.mki is missing."
	return 1
fi

################### some vars and functions for convenience ###################

# lset: Find exported env-vars whose names start with specific leading words
# Example:
#	$ lset gmu
#	gmu_LOG_OUTPUT_FILENAME=_gmulog.txt
#	gmu_DIR_ROOT=/home/chj/w/GMU
#	gmu_SUPPRESS_INCLUDE_NOT_FOUND_WARNING=1
#	gmu_MAKE_EXE=make-gmu
#	gmu_DO_SHOW_LINK_CMD=1
#	gmu_DIR_GNUMAKEUNIPROC=/home/chj/w/GMU/GMU-main/GnumakeUniproc
#	gmu_ver=0.99
# like a super Windows CMD 'set', so I name it "linux set".
lset(){
	for v in "$@"; do
		env | grep "^$v"
	done
}

lgmv(){
	lset gmu_
	lset gmp_
	lset gmi_
	lset gms_
	env | grep "^gv[0-9]"
}
# Note: I do not use one single regex because I would not be able to have gmu_ before gmp_ .

export gv1='gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'
export gv2='gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'
export gmuex1=$gmu_DIR_ROOT/GMU-examples/common/walkdir/make-all


echo "From ${BASH_SOURCE} export env-var:"
echo "    gmu_DIR_ROOT=$gmu_DIR_ROOT"
echo "    gv1=$gv1"
echo "    gv2=$gv2"
echo "Your PATH is prepended with: $gmu_DIR_ROOT/bin"

