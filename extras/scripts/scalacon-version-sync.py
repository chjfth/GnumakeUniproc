#!/usr/bin/env python

"""
Search for version numbers from input-file, modify(synchronize) output file(s) accordingly.

Input options:

--input=<input-file>

--add-datetime

--sig-vlinear=<sig>
	text signature indicating the linear version number.
	Example:
		For a line of text in input-file,
		
			enum { libfoo_nls_revision = 1234 };
		
		and you assign --sig-vlinear=nls_revision, then, 1234 will be recognized
		as the "linear version" resulting in a linear version string 
		
			nls_revision 1234
		
		So, in .rc ,there will be a line:
		
			VALUE "FileVersion",	"0.0.0.0 (nls_version 1234)\0"

Output options:

--mod-rc=<windows-resource-file>
Sync version info from <input-file> into .rc, checking key:
FILEVERSION, PRODUCTVERSION, "FileVersion", "ProductVersion" .

Rule:
For input file: search for string "vmajor", "vminor", "vbuild", "vextra", and,
the token passed as parameter --sig-vlinear, 
if found and followed by a number(intervening space,tab,*,/ allowed), that number
is extracted as version number.

For output file: Now support only Windows resource script(.rc).
The version number string following PRODUCTVERSION and FILEVERSION will be replaced.
"""

import sys
import getopt
import time
import re

version = "1.2"

vmajor = 0
vminor = 0
vbuild = 0
vextra = 0
vlinear = 0 # todo: renamed to vlinear
sig_vlinear = ''

g_isAddDatetime = False;
opts = {} # opts is a dictionary


datestr = time.strftime('%Y-%m-%d %H:%M:%S')

def get_optvallist(ar, optname): # ar is an array of 2-ele tuples
	retlist = []
	for t in ar:
		if (t[0] == optname): retlist.append(t[1])
	return retlist

def sync_windows_rc(ofn_rc):
	"""
	ofn_rc: .rc filename
	"""
	of_rc = open(ofn_rc, 'r+');
	if not of_rc:
		print 'Cannot open file %s for modification!'%(of_rc)

	lines = of_rc.readlines()
	for i in range(0, len(lines)): 
		line_old = lines[i]
		substyle1 = r'\1 %d,%d,%d,%d'%(vmajor,vminor,vbuild,vextra)
		lines[i] = re.sub(
			r'(^[ \t]*FILEVERSION).*', substyle1, 
			lines[i])
		lines[i] = re.sub(
			r'(^[ \t]*PRODUCTVERSION).*', substyle1,
			lines[i])

		substyle2 = r'\1"%d.%d.%d.%d%s%s\\0"'%(
			vmajor,vminor,vbuild,vextra, 
			' (%s %d)'%(sig_vlinear, vlinear) if vlinear else '',
			' (%s)'%(datestr) if g_isAddDatetime else '')
		lines[i] = re.sub(
			r'(VALUE[ \t]*"FileVersion"[, \t]+).+', substyle2,
			lines[i])
		lines[i] = re.sub(
			r'(VALUE[ \t]*"ProductVersion"[, \t]+).+', substyle2,
			lines[i])

		if (line_old != lines[i]):
			print 'Replaced %s(%d): %s'%(ofn_rc, i+1, lines[i])

	#print "Lines: %d" % (len(lines)) # Debug
	#for line in lines: print line,

	of_rc.truncate(0)
	of_rc.seek(0) 
		# I must seek() to 0 before writelines(), otherwise I'll get 00 00 00 ... at start of file.
	of_rc.writelines(lines)
	of_rc.close()


def main():
	global vmajor, vminor, vbuild, vextra, sig_vlinear, vlinear
	global opts
	global g_isAddDatetime

	optlist,arglist = getopt.getopt(sys.argv[1:], '', 
		['input=', 'mod-rc=', 'add-datetime', 'sig-vlinear=', 'version'])
	for opt in optlist:
		opts[opt[0]] = opt[1]

	if '--version' in opts:
		print 'version-sync.py v%s'%(version)
		exit(0)
	
	if '--add-datetime' in opts:
		g_isAddDatetime = True
	
	if '--sig-vlinear' in opts:
		sig_vlinear = opts['--sig-vlinear']

	if '--input' in opts:
		infilename = opts['--input']
	else:
		print 'Error: no --input=<input-file> assigned.'
		exit(1)
	
	# Add ofn_rcs from --mod-rc options
	ofn_rcs = get_optvallist(optlist, '--mod-rc')
		# ofn: output file name
	# Add ofn_rcs from command line arguments(arglist), those with .rc extname.
	for file in arglist:
		if re.match(r'.+\.rc$', file, re.IGNORECASE):
			ofn_rcs.append(file)
	
	##//
	#print infilename, ofn_rcs # debug

	infile = open(infilename, 'r')
	if not infile:
		print 'Cannot open file %s for read!'%(infilename)
		exit(2)

	lines = infile.readlines()
	infile.close();

	for line in lines:
		ptn_nummatch = '[ \t=/\*]+?([0-9x]+)'
		r = re.search('.+vmajor'+ptn_nummatch, line)
		if (r): vmajor = int(r.group(1), 0)

		r = re.search('.+vminor'+ptn_nummatch, line)
		if (r): vminor = int(r.group(1), 0)

		r = re.search('.+vbuild'+ptn_nummatch, line)
		if (r): vbuild = int(r.group(1), 0)

		r = re.search('.+vextra'+ptn_nummatch, line)
		if (r): vbuild = int(r.group(1), 0)

		if sig_vlinear:
			r = re.search('.+'+sig_vlinear+ptn_nummatch, line)
			if (r): vlinear = int(r.group(1), 0) # 2nd param 0 makes int() adaptable to '11' and '0x11', like C strtol().

	# Modify Windows .rc files below
	for ofn_rc in ofn_rcs:
		sync_windows_rc(ofn_rc)

if __name__ == '__main__':
    ret = main()
    exit(ret)
