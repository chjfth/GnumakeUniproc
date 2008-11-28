#!/bin/sh
#
# This shell script acts as the simple install process for installing
# required executable files for GnumakeUniproc on a Linux machine.
# After executing this install script, you should set some env-vars
# in order for GnumakeUniproc to work. These env-vars to set are listed 
# in set-gmuenv.sc , which you can `source'. 
#   I suggest you check the simple set-gmuenv.sc to know what env-vars
# it will set. If you are in haste, just cd to the dir where this 
# install-exe.sh resides and execute `source set-gmuenv.sc' , 
# then your env-vars are set.
#
# Two things are done in this script:
# 1. Compile and copy the gmuXXX programs to $DIR_GMU_PRG
# 2. Compile and copy the umake* scripts to $DIR_GMU_PRG, which is required 
#	by GNUmake 3.80(not required by GNUmake 3.81 or above).

DIR_GMU_PRG_SRC=gmu_programs
DIR_GMU_PRG=$1

if [ "$DIR_GMU_PRG" = "" ]; then
	echo "You must assign a direcotry as parameter, and GnumakeUniproc's\
 binaries will be copied there( e.g. /usr/local/bin )."
	exit 1
fi

if [ ! -d $DIR_GMU_PRG ]; then
	if mkdir $DIR_GMU_PRG; then true
	else echo "Cannot mkdir $DIR_GMU_PRG"; exit 1; fi
fi

GMU_PRGS="gmuAddActionWord gmuCountChar gmuExtractVarDefines"
for OnePrg in $GMU_PRGS; do
	echo "gcc -o $DIR_GMU_PRG/$OnePrg $DIR_GMU_PRG_SRC/$OnePrg/$OnePrg.c"
	if ! gcc -o $DIR_GMU_PRG/$OnePrg $DIR_GMU_PRG_SRC/$OnePrg/$OnePrg.c ; then
		exit 1
	fi
done

UMAKE_CMD="umake umakeD umakeU umakeUD"
for OnePrg in $UMAKE_CMD; do
	echo "cp umake_cmd/bash/$OnePrg $DIR_GMU_PRG/$OnePrg"
	if ! cp umake_cmd/bash/$OnePrg $DIR_GMU_PRG/$OnePrg ; then
		exit 1
	fi
done
