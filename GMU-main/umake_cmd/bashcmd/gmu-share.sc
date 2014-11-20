
# _gmu_rel2abs_path(): 
# Input a filepath(relative or absolute), return(echo) its absolute path.
# This function only does string operation. 
# This function will not change callers current working directory.
#
# Limitation:
# It cannot cope with non-usual path style like
#	dleft/../dright            (sandwiched ..)
#	dleft/./dright             (sandwiched .)
#	//my1///you2               (use multiple slashs)
#
gmu_rel2abs_path()
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


