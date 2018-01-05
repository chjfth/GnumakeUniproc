#!/bin/sh
#
# This shell script acts as the simple install process for installing
# required executable files for GnumakeUniproc on a Linux machine.
#
# Things done in this script:
# 1. Compile and copy the gmuXXX programs to $DIR_GMU_BIN
# 2. Copy precompiled make-gmu executable to $DIR_GMU_BIN. 


DIR_GMU_MAIN=$(\cd `dirname "$0"` && pwd)
	# So install-exe.sh must be placed in GMU-main directory
	# and DIR_GMU_MAIN will be an aboslute dir-path

DIR_GMU=${DIR_GMU_MAIN%/*}
	# the parent dir

DIR_GMU_BIN=$DIR_GMU/GMU-main/umake_cmd/bashcmd

echo "Directory \"$DIR_GMU_BIN\" will be used for GMU binary files."

DIR_GMU_BIN_SRC=$DIR_GMU_MAIN/gmu_programs

GMU_PRGS="gmuAddActionWord gmuCountChar gmuExtractVarDefines"
for OnePrg in $GMU_PRGS; do
	cmd="gcc -o $DIR_GMU_BIN/$OnePrg $DIR_GMU_BIN_SRC/$OnePrg/$OnePrg.c"
	echo "$cmd"
	if ! $cmd ; then
		exit 1
	fi
done


cmd="cp $DIR_GMU_MAIN/umake_cmd/make-linux-x86/make-gmu $DIR_GMU_BIN"
echo "$cmd"
if  ! $cmd ; then
	echo "Cannot copy make-gmu executable!"
	exit 1
fi

echo ""
echo "GMU installed OK!"
echo 'Remember to add'
echo ''
echo '    source $DIR_GMU/gmupath.sc
echo ''
echo 'to your .bashrc in order to execute umake commands.'
echo ''
