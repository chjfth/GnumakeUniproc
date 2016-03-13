#!/usr/bin/env python

"""
This py is called by program-generated __Makefile-cpuxm .

cpuxm: copy user examples

Actions by this program:

Analyze input file(INI, as arglist[0]),
* Check value of [globals]->sdkname (called @sdkname).
  If this value does not exist, assert error.
* Create the dir $gmb_syncto
* If @examples_dir is not null, 
  copy content inside '@examples_dir' into '$gmb_syncto/@examples_copyto'
  .
  If examples_dir is a relative dir, it is relative to the INI file.

Input summary:

--gmb_syncto=<synctodir>
	Tells where to synchronize the files(the destination).

arglist[0]
	The INI filename.

Thanks to:
http://stackoverflow.com/questions/4276255/os-walk-exclude-svn-folders
http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows/1214935#1214935
"""

import sys
import getopt
import re
import os
import shutil
import errno
import stat
import ConfigParser

version = "1.2"

opts = {}
gmb_syncto = ''
examples_dir = ''
examples_copyto = ''

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise


def RemoveDotSvn(rootdir):
	for root, subFolders, files in os.walk(rootdir):
	  try:
	    subFolders.remove('.svn')
	    shutil.rmtree(root+'/.svn', onerror=handleRemoveReadonly)
	  except ValueError: # .svn subdir not exist
	    pass


def CopyExamples():
	dirDest = gmb_syncto + '/' + examples_copyto
	# copytree() requires that dirDest does not exist yet, so rmtree first.
	# And note: GNU make(at least 3.82) only compares file modification time, not creation time.
	if os.path.isdir(dirDest):
		shutil.rmtree(dirDest)
	shutil.copytree(examples_dir, dirDest, ignore=shutil.ignore_patterns('.svn', '.hg'))

def main():
	global opts, examples_dir, examples_copyto, gmb_syncto;
	fConfig = '' # the config file(in INI format)
	
	optlist,arglist = getopt.getopt(sys.argv[1:], '', ['gmb_syncto=', 'version'])
	opts = dict(optlist)

	if '--version' in opts:
		print '%s v%s'%(os.path.basename(__file__), version)
		return 0;

	if '--gmb_syncto' in opts:
		gmb_syncto = opts['--gmb_syncto']
	else:
		print 'Error: No --gmb_syncto=<synctodir> option assigned.'
	
	if(len(arglist)==0):
		print 'No input file! This program requires an INI file input.'
		return 1;

	fConfig = os.path.abspath(arglist[0]) # the INI filepath

	# Open config file(INI) 
	config = ConfigParser.ConfigParser()
	try:
		readret = config.read(fConfig)
	except(MissingSectionHeaderError):
		print "Error: %s seem not to be a valid configuration file."%(fConfig)
		return 2

	if not readret:
		print 'Error: The config file %s does not exist or cannot be opened.'%(fConfig)
		return 3

#	try:
#		sdkname = config.get('global', 'sdkname')
#	except:
#		print 'Error: In %s, no \'sdkname\' defined in [global] section.'%(fConfig)
#		return 4

	try:
		examples_dir = config.get('global', 'examples_dir')
		if not os.path.isabs(examples_dir):
			# Consider examples_dir relative to the INI file, now get its abspath for later use.
			examples_dir = os.path.join(os.path.split(fConfig)[0], examples_dir)
			examples_dir = os.path.abspath(examples_dir)
	except:
		examples_dir = ''

	if examples_dir:
		try:
			examples_copyto = config.get('global', 'examples_copyto')
		except:
			print 'Error: In "%s", you assign values for examples_dir, but does not assign examples_copyto yet.'%(fConfig)

		# Create necessary output dir.
		if not os.path.isdir(gmb_syncto):
			try:
				os.makedirs(gmb_syncto)
			except:
				print 'Error: Cannot create directory: '+ gmb_syncto
				if not os.path.isabs(gmb_syncto):
					print '  Absolute directory path is: ' + os.path.abspath(gmb_syncto)
				return 5

		CopyExamples()

	
#	RemoveDotSvn(gmb_syncto)
		# This is no longer necessary for svn 1.7+

	return 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
