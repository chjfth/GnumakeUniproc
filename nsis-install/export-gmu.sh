# This shell script exports GnumakeUniproc data from GnumakeUniproc's SVN repository for using on Linux.
# [2007-03-02] Currently, the prefix from sf.net is (use as $1)
#   https://gnumakeuniproc.svn.sourceforge.net/svnroot/gnumakeuniproc
# (chj internal use): 
#		https://nlssvn/svnreps/makingsys/GnumakeUniproc
# Tested with svn 1.4.2 (r22196)

source $(dirname $0)/export-share.sc # get var finaloutput

if [ "$1" == "" ]; then
	echo "You must assign a param as the SVN Url prefix for GnumakeUniproc SVN repository, and optionally a second param for branch to export(default to trunk)."
	exit 1
fi

SvnUrlPrefix=$1

BranchToGet=trunk

if [ "$2" != "" ]; then
	set BranchToGet=$2
fi

OutputDir=GMU

svn export --force $SvnUrlPrefix/$BranchToGet $OutputDir
ret=$?
if [ "$ret" != 0 ]; then
	echo "Unexpected! SVN export($1) failed."
	exit 1
fi

echo "All files of GnumakeUniproc have been retrieved."

echo "Packing $finaloutput ..."
tar jcf "$finaloutput" GMU
if [ "$?" != 0 ]; then echo "Packing $finaloutput failed!"; fi;

echo "Done."
