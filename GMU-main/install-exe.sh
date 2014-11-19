#!/bin/sh
#
# This shell script acts as the simple install process for installing
# required executable files for GnumakeUniproc on a Linux machine.
# After executing this install script, you should set some env-vars
# in order for GnumakeUniproc to work. These env-vars to set are listed 
# in set-gmuenv.sc , which you can `source'. 
#   I suggest you check the simple set-gmuenv.sc to know what env-vars
# it will set. 
#
# Two things are done in this script:
# 1. Compile and copy the gmuXXX programs to $DIR_GMU_PRG
# 2. Compile and copy the umake* scripts to $DIR_GMU_PRG. 

# _gmu_rel2abs_file(): 
# Input a filepath(relative or absolute), return(echo) its absolute path.
# This function only does string operation. 
# This function will not change callers current working directory.
_gmu_rel2abs_file()
{
	if [ "${1%%/*}" = "" ]; then 
		# $1 starts with a / , so it is already a absolute path.
		echo $1
		return
	fi

	dirGo="$PWD"
	dirRel="$1"
	
	# Strip preceeding ./ if any
	while [ "${dirRel#./}" != "${dirRel}" ]; do dirRel="${dirRel#./}"; done

	# Now we process possible ../.. prefix at the beginning of $1
	while [ "${dirRel#../}" != "${dirRel}" ]; do
		dirRel="${dirRel#../}"
		dirGo="${dirGo%/*}"
	done

	if [ "${dirRel}" = ".." ]; then 
		echo "${dirGo%/*} "
	else
		echo "${dirGo}/${dirRel}"; 
	fi
}

DIR_GMU_MAIN="${0%/*}"
	# So install-exe.sh must be placed in GMU-main directory

DIR_GMU=${DIR_GMU_MAIN%/*}
	# the parent dir

DIR_GMU_PRG=$1
	# Place of GMU binary. User can assign this explicitly(but optional)

if [ "$DIR_GMU_PRG" = "" ]; then
	DIR_GMU_PRG=$DIR_GMU/bin
fi

echo "Directory \"$DIR_GMU_PRG\" will be used for GMU binary files."
ln -s "$DIR_GMU_MAIN/umake_cmd/bashcmd" "$DIR_GMU_PRG"
if [ $? != 0 ]; then
	echo "ERROR: \"$DIR_GMU_PRG\" creation fail!"
fi

DIR_GMU_PRG_SRC=$DIR_GMU_MAIN/gmu_programs

GMU_PRGS="gmuAddActionWord gmuCountChar gmuExtractVarDefines"
for OnePrg in $GMU_PRGS; do
	cmd="gcc -o $DIR_GMU_PRG/$OnePrg $DIR_GMU_PRG_SRC/$OnePrg/$OnePrg.c"
	echo "$cmd"
	if ! $cmd ; then
		exit 1
	fi
done


cmd="cp $DIR_GMU_MAIN/umake_cmd/make-linux-x86/make-gmu $DIR_GMU_PRG"
echo "$cmd"
if  ! $cmd ; then
	echo "Cannot copy make-gmu executable!"
	exit 1
fi

echo ""
echo "GMU installed OK!"
echo "Remember to add '$DIR_GMU_PRG' to your PATH in order to execute umake commands."
