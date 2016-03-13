#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
基于一个 Scalacon 函数库源码树模版来生成一个具体的函数库源码目录树。

输入参数：

--name=<repo-name>
--repo=<repo-name>
	指出你要创建的这个 repository 的名字，这个名字会影响自动生成的一系列文件名、
	目录名、以及文件内容。
	-
	两个参数含义相同，选一即可。--repo 是老名字，不建议使用。


--dir-tmpl=<dirtmpl>
	指出模版处于何（本地）目录中。
	若为空，则默认为 $(gmu_DIR_ROOT)/nlscan/cprjtmpl/librepo2011
	
	当前用的模版来源：
	https://nlssvn/svnreps/makingsys/GMU-addons/trunk/nlscan/cprjtmpl/librepo2011

--dir-nlssvn=<dirNlssvn>
	指出 NLSSVN 本地根目录。

--rir-repo=<rirRepo>
	指出当前要创建的仓库（repository）相对于 NLSSVN 的目录。

--pure-c
	指出生成的模版里头源码为 .c 而非 .cpp 。不加此选项，默认是 .cpp 。

使用注意：
* 该程序需要 Python 2.6 以上。（但Python 3.0不行）
* 该程序依赖 Cheetah ，得将 Cheetah 安装在 Python 环境中。 http://www.cheetahtemplate.org/

"""

import sys
import getopt
import datetime
import os
import shutil
import errno
import stat
import re
#import ConfigParser
from Cheetah.Template import Template

version = "1.1"

opts = {}

g_is_pure_c = False

#dirTmpl = ''
#dirNlssvn = ''
#rirRepo = ''

def MyMakeDir(dir):
	if os.path.isdir(dir):
		return True

	try:
		os.makedirs(dir)
	except:
		print 'Error: Cannot create directory: '+ dirRepo
		if not os.path.isabs(dirRepo):
			print '  Absolute path is: ' + os.path.abspath(dirRepo)
		return False

	return True

def ReplaceFileStr(s, dic):
	"""
	s is a filename or dirname on filesystem
	Replace s according to dictionary dic.
	Example:
		dic = { 'repo'=walkdir }
		s = 'lib_@(repo)_dsp'
	s will become:
		'lib_walkdir_dsp'
	"""
	for key in dic:
		s = s.replace('@(%s)'%key , dic[key])
	return s

def Copy1FileFromTemplate(ipath, opath, dicSubst):
	"""
	ipath, opath are both filepath.
	"""
	tpl = Template(file=ipath, searchList=[dicSubst])
	outstr = str(tpl)
	
	odir = os.path.split(opath)[0]
	if not MyMakeDir(odir):
		return False
	
	try:
		fh = open(opath, 'w')
		fh.write(outstr)
		fh.close()
	except:
		print 'Cannot create and write to file: %s'%(opath)
		return False
	
	return True

def NormalizeCFuncName(name):
	"""
	Fix characters that cannot form a legal C function name.
	"""
	for c in r'-+`~!@#$%^&*()=|\[]{};\':",./<>?':
		name = name.replace(c, '_')
	if name[0] in '0123456789':
		name = '_'+name
	return name

def CreateRepo(repo, dirTmpl, dirNlssvn, rirRepo):
	# repo: The given repository name
	
	# Create destination folder
	if dirNlssvn:
		dirRepo = dirNlssvn + '/' + rirRepo
	else:
		dirRepo = repo
	
	if not MyMakeDir(dirRepo):
		return False

	dicSubst = { 'bs': '\\' }
		# so, you can use $(bs) to represent a backslash char in your template file,
		# to avoid escaping the very Cheetah directive char($, #) right behind.
	dicSubst['dirNlssvn'] = dirNlssvn
	dicSubst['repo'] = repo
	dicSubst['repo_'] = NormalizeCFuncName(repo)
	dicSubst['exe_repo'] = 'exe_'+repo
	dicSubst['exe_repo_'] = 'exe_'+NormalizeCFuncName(repo)
	dicSubst['exe_repo_usedll'] = 'exe_'+repo+'_usedll'
	dicSubst['exe_repo_usedll_'] = 'exe_'+NormalizeCFuncName(repo)+'_usedll'
	dicSubst['cpp'] = 'c' if g_is_pure_c else 'cpp'
	rela = os.path.relpath('.', rirRepo)
	dicSubst['dirNlssvnRRR'] = rela.replace('\\', '/')
	dicSubst['dirNlssvnRRRBs'] = rela.replace('/', '\\')
	dicSubst['timeYYYYMMDD'] = datetime.date.today().strftime('%Y%m%d')

	# Walk through dirTmpl ...
	for root, folders, files in os.walk(dirTmpl):
		for ifile in files:
			# ipath: input filepath; opath: output filepath
			ipath = root + '/' + ifile
			if ifile[-5:]=='.tmpl':
				opath = dirRepo + root[len(dirTmpl):] + '/' + ifile[:-5]
				opath = ReplaceFileStr(opath, dicSubst)
				if not Copy1FileFromTemplate(ipath, opath, dicSubst):
					return False
			else:
				opath = dirRepo + root[len(dirTmpl):] + '/' + ifile
				opath = ReplaceFileStr(opath, dicSubst)
				try:
					MyMakeDir(os.path.split(opath)[0])
					shutil.copy(ipath, opath)
				except:
					print "Cannot copy tree '%s' to '%s' !"%(os.path.normpath(ipath), os.path.normpath(opath))
					return False
		
		if '.svn' in folders:
			folders.remove('.svn')


def AssertMissingOpt(reqopts):
	global opts
	# reqopts can be '--xxx=' or '--xxx'
	reqoptschk = [ '--'+(opt[:-1] if opt[-1]=='=' else opt) for opt in reqopts]
	for opt in reqoptschk:
		if not opt in opts:
			print 'Error: No %s option assigned.'%(opt)
			return False
	return True

def main():
	global opts, g_is_pure_c #, dirTmpl, dirNlssvn, rirRepo

	# Scan all arguments, replace --name= to --repo= . (todo: searching a more effect way)
	for i in range(0, len(sys.argv)):
		sys.argv[i] = re.sub(r'--name=', r'--repo=', sys.argv[i])

	reqopts = ['repo=']
	optlist,arglist = getopt.getopt(sys.argv[1:], '', 
		['repo=', 'dir-tmpl=', 'dir-nlssvn=', 'rir-repo=', 'pure-c', 'version'])
	for opt in optlist:
		opts[opt[0]] = opt[1]

	if '--version' in opts:
		print '%s v%s'%(os.path.basename(__file__), version)
		return 0

	if not AssertMissingOpt(reqopts):
		return 1
	
	repo = opts['--repo']
	
	try:
		dirTmpl = opts['--dir-tmpl']
	except:
		dirTmpl = ''

	try:
		dirNlssvn = opts['--dir-nlssvn']
	except:
		dirNlssvn = ''
		
	try:
		rirRepo = opts['--rir-repo']
	except:
		rirRepo = ''
	
	if '--pure-c' in opts:
		g_is_pure_c = True
	
	if dirTmpl:
		if not os.path.isdir(dirTmpl):
			print "Error: '%s' is not an existing directory!"%(dirTmpl)
			return 2
	else:
		dirGmu = ''
		# Try to use default template directory
		try:
			dirGmu = os.environ['gmu_DIR_ROOT']
		except:
			print "Error: You do not assign --dir-tmpl option, "\
				"and Env-var gmu_DIR_ROOT is not defined either,"\
				"So I don't have a repository template to work on."
			return 2

		rirTmpl = '/nlscan/cprjtmpl/librepo2011'
		dirTmpl = dirGmu + rirTmpl
		print '--dir-tmpl option not assigned, using default: %s'%(dirTmpl)
		if not os.path.isdir(dirTmpl):
			print "Error: '%s' is not an existing directory!"%(dirTmpl)
			return 1
	
	if dirNlssvn and not os.path.isdir(dirNlssvn):
		print "Error: Your NLSSVN root dir '%s' does not exist yet! You have to create it first."%(dirNlssvn)
		return 2

	b = CreateRepo(repo, dirTmpl, dirNlssvn, rirRepo)

	return 4 if not b else 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
