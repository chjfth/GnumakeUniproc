#!/usr/bin/env python

"""
For input files, find a line of content(called signature):
	#define DLL_AUTO_EXPORT_STUB
If found, append a line

void <expfx>__<thisfile>__DLL_AUTO_EXPORT_STUB() { }
or
extern"C" void <expfx>__<thisfile>__DLL_AUTO_EXPORT_STUB(){}

Note: <thisfile> defaults to the input file stem name(i.e. ext name stripped).
But if <expfx>__<thisfile> has been manually written to be something else, respect it,
and I will not replace it with true <expfx>__<thisfile>.

Output(to stdout): A series of lines. Each line is
* the export-stub function name, if it exports;
* a . character if it does not export.

Options:
	--extra-prefix=<expfx>
		Extra prefix to add to export-stub functions name.
		<expfx> is added only when the name is selected automatically.
		
	--mute
		Will not write anything to stdout. The net effect is: just tamper .c/.cpp .
"""

import sys
import getopt
import re
import os

version = "1.0"

opts = {}

g_isMute = False
g_extra_prefix = ''

def NormalizeCFuncName(name):
	"""
	Fix characters that cannot form a legal C function name.
	"""
	for c in r'-+`~!@#$%^&*()=|\[]{};\':",./<>?':
		name = name.replace(c, '_')
	if name[0] in '0123456789':
		name = '_'+name
	return name

def ExportStubFuncName(prefix, stem):
	return NormalizeCFuncName(prefix + stem + "__DLL_AUTO_EXPORT_STUB")

def ProcessOneFile(fname):
	isFoundSignature = False;
	export_funcname = '.' # . means no export function name
	fh = open(fname, 'r+')
	lines = fh.readlines()
	
	# Extract stem name from filename.
	m = re.search(r'([^/]+).(c|cpp)$', fname, re.IGNORECASE)
	if not m:
		print "export-tamper.py: %s is not a C/C++ file!\n"%(fname)
		# sys.stderr.write // Sorry, stderr seems to get captured by os.popen, and I don't know how to grab that out.
		return None
	
	stemname = m.group(1);
	dft_insert = 'void ' + ExportStubFuncName(g_extra_prefix, stemname) + '(void){}\n'
		# default C statement to insert
	
	if m.group(2) == 'cpp':
		dft_insert = 'extern"C" ' + dft_insert
	
	nline = len(lines)
	for i in range(0, nline):
		m = re.match(r'^[ \t]*#define[ \t]+DLL_AUTO_EXPORT_STUB', lines[i]);
		if m: 
			isFoundSignature = True
			break;
		
	if isFoundSignature:
		# Add export-stub function statement(if not there yet) and get that function name(export_funcname)
		isInsertNew = False
		if i < nline-1: # "#define DLL_AUTO_EXPORT_STUB" is not at the final line
			# check whether export-stub function has been there
			m = re.search(r'void[ \t]+([A-Za-z0-9_]+__DLL_AUTO_EXPORT_STUB)', lines[i+1])
			if m: # the line to add is already there
				export_funcname = m.group(1)
			else:
				export_funcname = ExportStubFuncName(g_extra_prefix, stemname)
				isInsertNew = True
		else:
			if lines[i][-1] != '\n': # the final line is not ended with \n
				lines[i] += '\n'
			export_funcname = ExportStubFuncName(g_extra_prefix, stemname)
			isInsertNew = True
		
		if isInsertNew:
			lines.insert(i+1, dft_insert)
			fh.seek(0)
			fh.writelines(lines)
	
	if not g_isMute:
		print export_funcname
	
	fh.close();

def main():
	global opts
	global g_isMute, g_extra_prefix
	
	optlist,arglist = getopt.getopt(sys.argv[1:], '', ['mute', 'extra-prefix=', 'version'])
	for opt in optlist:
		opts[opt[0]] = opt[1]

	if '--version' in opts:
		print 'export-tamper.py v%s'%(version)
		return 0;
	
	if '--mute' in opts:
		g_isMute = True
		
	if '--extra-prefix' in opts:
		g_extra_prefix = opts['--extra-prefix']

	if(len(arglist)==0):
		print 'No input file!'
		return 1;
	
	for fname in arglist:
		ProcessOneFile(fname)
	
	return 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
