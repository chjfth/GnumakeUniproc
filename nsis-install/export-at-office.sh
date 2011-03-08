# If I'm in nlscan office, just call this bat to export ALL files necessary
# to pack a GnumakeUniproc Linux release suitable for NLSCAN staff.

./export-gmu.sh https://nlssvn/svnreps/makingsys/GnumakeUniproc
if [ "$?" != 0 ]; then
	echo "SVN export failed!"
	exit 1
fi

./export-nlscan.sh https://nlssvn/svnreps/makingsys
if [ "$?" != 0 ]; then
	echo "SVN export failed!!"
	exit 1
fi

echo All exports success.

finaloutput=GMU.tar.bz2
echo "Packing NLSCAN extras to $finaloutput ..."
tar jcf $finaloutput GMU
if [ "$?" == 0 ]; then 
	echo "Done $finaloutput successfully."
	exit 0
else
	echo " Failed!";
fi
