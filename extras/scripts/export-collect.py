#!/usr/bin/env python

"""
Launch export-tamper.py to process all input .c/.cpp files, check whether they have
	#define DLL_AUTO_EXPORT_STUB
, if yes, collect the export-stub function name(on the very following line) into <upfile>.

Options:

--prjname=<prjname>
	(optional)
	Tells the GMU project name of current project.
	If not given, it is empty.

--update=<upfile>
	Output file for the collected function names.
	Each line in <upfile> has the format:
	
		[prjname]:<function-name>

"""

import sys
import getopt
import re
import os

version = "1.0"

NoExportStubSig = '.'

opts = {}

def ProcessOneFile(fname, prjname, funcnames):
	
	fhinput = os.popen('export-tamper.py '+fname)
	strret = fhinput.readline()
	if strret[0] == NoExportStubSig:
		None # Do nothing
	elif strret: # got some funtion name
		funcnames.append(prjname + ':' + strret)
	else:
		print("Unexpected! export-tamper.py execution error!")
		exit(2)
	

def main():
	global opts;
	prjname = ''
	
	optlist,arglist = getopt.getopt(sys.argv[1:], '', ['prjname=', 'update=', 'version'])
	for opt in optlist:
		opts[opt[0]] = opt[1]

	if '--version' in opts:
		print('export-collect.py v%s'%(version))
		print('Example:')
		print('  export-collect.py --update=<upfile> foo1.c foo2.c foo3.cpp ...')
		return 0;
	
	if(len(arglist)==0):
		print('No input file!')
		return 1;
	
	if not '--update' in opts:
		print('No --update==<upfile> assigned!')
		return 2;
	
	if '--prjname' in opts:
		prjname = opts['--prjname']

#	print('>>>' + opts['--update'])
	fnupdate = opts['--update']
	
	fhupdate = open(fnupdate, 'w')
	lines = []
	
	for fname in arglist:
		ProcessOneFile(fname, prjname, lines)
		
	fhupdate.writelines(lines)
	fhupdate.close();
	
	return 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
