
export tmpbatdir=$(\cd `dirname ${BASH_SOURCE}` && pwd)

export NLSSVN=https://nlssvn/svnreps
_gmuex1=%tmpbatdir%\GMU-examples\common\walkdir\make-all

export gv1='gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'
export gv2='gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'

PATH=$gmu_DIR_ROOT/bin:

echo "From ${BASH_SOURCE} export env-var:"
echo "    gv1=$gv1"
echo "    gv2=$gv2"
echo "And your PATH is prepended with: \"$gmu_DIR_ROOT/bin\""

