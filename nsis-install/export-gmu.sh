# This shell script exports GnumakeUniproc data from GnumakeUniproc's SVN repository for using on Linux.
# [2007-03-02] Currently, the prefix from sf.net is (use as $1)
#   https://gnumakeuniproc.svn.sourceforge.net/svnroot/gnumakeuniproc
# (chj internal use): 
#		https://nlssvn/svnreps/makingsys/GnumakeUniproc
# Tested with svn 1.4.2 (r22196)

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


function Checkout1Module()
{
	svn export --force $SvnUrlPrefix/$1/$BranchToGet $OutputDir/$1
	ret=$?
	if [ "$ret" != 0 ]; then
		echo "Unexpected! SVN export($1) failed."
	fi
	return $ret
}

Checkout1Module GMU-main;      if [ "$?" != 0 ]; then exit 1; fi;
Checkout1Module GMU-manual;    if [ "$?" != 0 ]; then exit 1; fi;
Checkout1Module GMU-ext;       if [ "$?" != 0 ]; then exit 1; fi;
Checkout1Module GMU-examples;      if [ "$?" != 0 ]; then exit 1; fi;
Checkout1Module demo-repositories; if [ "$?" != 0 ]; then exit 1; fi;
Checkout1Module nsis-install;      if [ "$?" != 0 ]; then exit 1; fi;

echo "All files of GnumakeUniproc have been retrieved."

echo "Packing GMU.tar.bz2 ..."
tar jcf GMU.tar.bz2 GMU
if [ "$?" != 0 ]; then echo "Packing GMU.tar.bz2 failed!"; fi;

echo "Done."