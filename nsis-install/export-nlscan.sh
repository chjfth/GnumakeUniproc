#
# Special: For convenience, I export NLSCAN related files and pack them into GMU.
#	https://nlssvn/svnreps/makingsys
if "$1" == "xx"; then
	echo "You must assign a param as the SVN Url prefix for SVN repository, and optionally a second param for branch to export(default to trunk)."
fi

SvnUrlPrefix=$1

BranchToGet=trunk

if  "$2" != ""; then BranchToGet=$2; fi

OutputDirGMU=./GMU

svnurl=$SvnUrlPrefix/GMU-addons/$BranchToGet/nlscan
echo "SVN exporting $svnurl ..."
svn export --force $svnurl $OutputDirGMU/nlscan
if [ "$?" != 0 ]; then
	echo "Unexpected! SVN export($svnurl) failed."
	exit 1
fi

svnurl=$SvnUrlPrefix/GMU-addons/$BranchToGet/scripts
echo "SVN exporting $svnurl ..."
svn export --force $svnurl $OutputDirGMU/bin
if [ "$?" != 0 ]; then
	echo "Unexpected! SVN export($svnurl) failed."
	exit 1
fi

echo "NLSCAN related files have been retrieved."

