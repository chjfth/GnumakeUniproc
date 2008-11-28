[2007-10-03] CVS repository created with CVS 1.12.12, on SuSE Linux 10.1.

Memo:

cvs -d /soft/2007ALLGMU/demo-repositories/trunk/cvsreps-zlib-demo init

mkdir /soft/2007t; cd /soft/2007t

GMUBASE=svn://192.168.11.1/GnumakeUniproc
svn export $GMUBASE/demo-repositories/trunk/svnreps-zlib
svn export $GMUBASE/demo-repositories/trunk/svnreps-zlib-example
svn export $GMUBASE/demo-repositories/trunk/svnreps-zlib-minigzip
# The checkout content of the above three command are three demo svn reps.

# Then checkout C code from the above three demo svn reps:
svn export file:///soft/2007t/svnreps-zlib/trunk zlib
svn export file:///soft/2007t/svnreps-zlib-example/trunk zlib-example
svn export file:///soft/2007t/svnreps-zlib-minigzip/trunk zlib-minigzip

cd zlib
cvs -d /soft/2007ALLGMU/demo-repositories/trunk/cvsreps-zlib-demo import -m "import cvs module zlib" zlib tvendor trelease
cd ../zlib-example
cvs -d /soft/2007ALLGMU/demo-repositories/trunk/cvsreps-zlib-demo import -m "import cvs module zlib-example" zlib-example tvendor trelease
cd ../zlib-minigzip
cvs -d /soft/2007ALLGMU/demo-repositories/trunk/cvsreps-zlib-demo import -m "import cvs module zlib-minigzip" zlib-minigzip tvendor trelease