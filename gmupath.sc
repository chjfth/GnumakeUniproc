# Will set tmpdir to gmu-root
tmpdir=$(\cd `dirname ${BASH_SOURCE}` && pwd)

export NLSSVN=https://nlssvn/svnreps
_gmuex1=$tmpdir/GMU-examples/common/walkdir/make-all

export gv1='gmu_DO_SHOW_VERBOSE=1 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'
export gv2='gmu_DO_SHOW_VERBOSE=2 gmu_DO_SHOW_COMPILE_CMD=1 gmu_DO_SHOW_LINK_CMD=1'

# Will set tmpdir to bashcmd
tmpdir=$tmpdir/GMU-main/umake_cmd/bashcmd

PATH=$tmpdir:$PATH

echo "From ${BASH_SOURCE} export env-var:"
echo "    gv1=$gv1"
echo "    gv2=$gv2"
echo "And your PATH is prepended with: \"$tmpdir\""

