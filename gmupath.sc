# Will set tmpdirgmu to gmu-root
tmpdirgmu=$(\cd `dirname ${BASH_SOURCE}` && pwd)

export NLSSVN=https://nlssvn.dev.nls/svnreps
_gmuex1=$tmpdirgmu/GMU-examples/common/walkdir/make-all

export gv1='gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'
export gv2='gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'

export gmu_INTERACTIVE_ERROR_RETRY=1

# Will set tmpdirgmu to bashcmd
tmpdirgmu=$tmpdirgmu/extras/scripts:$tmpdirgmu/GMU-main/umake_cmd/bashcmd

PATH=$tmpdirgmu:$PATH

echo "From ${BASH_SOURCE} export env-var:"
echo "    gv1=$gv1"
echo "    gv2=$gv2"
echo "And your PATH is prepended with: \"$tmpdirgmu\""

