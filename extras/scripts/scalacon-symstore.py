#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
该程序调用微软 Debugging Tools for Windows 中的 symstore add ... 来往符号仓库中添加扫描到的
可用文件（dll, pdb），相当于是 symstore 的一个包装（wrapper）。

用这个包装的好处：

【好处一】
symstore 的通配符支持很差，你只能指定处理 D:\somdir\*.pdb 或 D:\somdir\*.dll 或……，总之，
只能指定一茬，你无法要求处理 *.pdb 但忽略 *.lib.pdb 。

用 scalacon-symstore.py，我们可以自己扫描目录，找出需要处理的文件，将此文件存成一个响应文件
symfile-scan.txt，再用 /f @symfile-scan.txt 传给 symstore，就能准确告知应处理哪些文件。

【好处二】
当 symstore 中途出错时，它的退出码有可能仍是 0，导致调用者无法得知它是否出错了，
案例见 http://webs.dev.nls:8080/pages/viewpage.action?pageId=51511441 。

==========典型错误样本
C:\>symstore add /y c:\Users\chj\chji.txt /g C:\Users\chj\build /s \\winshad0\devshare\NlsSymbols /t
 testy /o
SYMSTORE MESSAGE: LastId.txt reported id 11
SYMSTORE MESSAGE: Final id is 0000000011
SYMSTORE MESSAGE: Copying C:\Users\chj\build\aq\aqpm.pdb to \\winshad0\devshare\NlsSymbols\aqpm.pdb\8728C1A900254F9AAF0E0FC822785A412\aqpm.pdb [Force: T, Compress: F]
SYMSTORE ERROR: Class: Runtime. Desc: Failed to copy C:\Users\chj\build\aq\aqpm.pdb to server Error64: The specified network name is no longer available.

SYMSTORE: Number of files stored = 0
SYMSTORE: Number of errors = 1
SYMSTORE: Number of files ignored = 0
==========

更多错误情形： http://webs.dev.nls:8080/pages/viewpage.action?pageId=51511494

因此，用 scalacon-symstore.py，我们就可以检查 symstore 的输出，查找“Number of errors”来判断，
而且，若有错误，还要找出是哪个文件出错了，并重试之。
我们检查 Failed to copy XXX 来揪出错误文件，并且，重新组织一个响应文件让其重试。
不要用原始的 symfile-scan.txt 来重试，那会导致，即使只有一个文件错误，也要全部文件重新都 store 一遍。

（2011-09-02）当前针对的 symstore 版本：6.11.404.1 (2009)

输入参数：

--dir-scan=<dscan>
	[必须]
	指出在哪个目录中搜索 sym 文件，对应 symstore /f 。
	递归搜索子目录，硬行为。

--dir-store=<dstore>
	[必须]
	指出 symbol store 目录（写入目录），对应 symstore /s 。

--3tier-symstore
	[可选]
	如果指定，当 <dstore> 目录原先不存在、或是空目录时，本程序会先在 <dstore> 中创建 index2.txt 
	以便 symstore.exe 能生成“三层”symbol store 的目录结构

--product-name=<prodn>
	[可选]
	指出“产品名称”，对应 symstore /t

--product-ver=<prodv>
	[可选]
	指出“产品版本”，对应 symstore /v

--pattern-include=<ptinc>
	[可选]
	告知要扫描哪些类型的文件。若不指定，相当于指定了 *.pdb/*.exe/*.dll/*.sys 。
	文件类型基于“通配符”，内部用 fnmatch 实现。比如 * 表示匹配0个或多个任意字符，? 表示匹配单个字符。
	通配符描述的是文件名，而非带目录前缀的文件路径。比如，不能用 vc80/*.pdb 来指定仅查找处于 vc80 子目录中的 *.pdb。
	若要指定多组通配符，则用 / 分隔开。如，扫描所有 dll 和 pdb，则指定 --pattern-include=*.dll/*.pdb

--pattern-exclude=<ptexc>
	[可选]
	告知要排除的文件通配符。
	该参数的用意是在 --pattern-include 指定的文件中排除掉一些文件。 Scalacon 上常用案例是，
	要求扫描 *.pdb 但排除 *.lib.pdb ，则参数可写为：
		--pattern-include=*.pdb --pattern-exclude=*.lib.pdb

--tmpdir=<tmpdir>
	[可选]
	存放临时文件的目录。若不提供，就用当前目录。
	临时目录中会生成如下文件：
	1. 传给 symstore.exe 的响应文件会被生成于此目录中。
	2. symstore 的 logfile（symstore /d <tmpdir>）

--max-retry=<maxretry>
	[可选]
    指出允许 symstore 可以重试几次。默认为 3 次。0 表示不重试。
    当用 symstore 处理一个很大的源目录，且存储目标是网络共享文件夹时，失败比较可能
    会发生，因此我设计了代码让 symstore 能够重试。当然每次重试会导致生成一个
    新的 symstore ID。
    另，本程序会分析 symstore /o 的输出，自动找出哪些文件已经存储成功，因此，
	重试时只会让 symstore 处理未成功的那些文件。

--allow-empty-scan
	[可选]
	无文件被操作时仍旧返回成功（退出码 0）。

【限制】
1. dscan 目录不允许有空格。

【备注】
惊讶：
1. os.walk() 可以处理 UNC 路径（如 \\winshad0\devshare），因此 dscan 和 dstore 可以处理 UNC 路径。
"""

import sys
import getopt
import datetime
import os
import shutil
import errno
import re
import subprocess
import tempfile
import fnmatch
#import ConfigParser

version = "1.2"

opts = {}

g_dscan = ''
g_dstore = ''

g_prodn = 'Unknown-prodname'
g_prodv = 'Unknown-prodver'

g_tmpdir = '.'
g_maxretry = 3

gar_ptinc = ['*.pdb', '*.exe', '*.dll', '*.sys']
	# gar means global array.
gar_ptexc = ['vc?0.pdb', 'vc??0.pdb', '*.lib.pdb*'] 
	# Exclude those vc60.pdb, vc80.pdb, vc100.pdb .

g_allow_empty_scan = False

ErrNoFileProcessed = 9

f_ssinput = 'ssinput.txt'

def AssertMissingOpt(reqopts, is_print_errmsg=True):
	global opts
	# reqopts can be '--xxx=' or '--xxx'
	reqoptschk = [ '--'+(opt[:-1] if opt[-1]=='=' else opt) for opt in reqopts]
	for opt in reqoptschk:
		if not opt in opts:
			if is_print_errmsg:
				print 'Error: No %s option assigned.'%(opt)
			return False
	return True

def CallSymstore_with_filelist(in_pathlist, retry=0):
	"""
	in_pathlist: input file list, in array
	retry: a number, if retry > 0, a retry suffix is added to response-file filename.

	Return: a tuple,
		[0] symstore final id in string format ,e.g. "0000000011"
		[1] list of failed files, in array
	"""
	# Write file list to the response-file
	tmpdir = opts['--tmpdir'] if '--tmpdir' in opts else '.'
	retry_suffix = '' if retry==0 else '-retry%d'%retry

	tmp_ssf = tmpdir+'/'+f_ssinput + retry_suffix
	of = open(tmp_ssf, "wb+")
	if not of:
		print "Error: Cannot create symstore input-response-file: %s !"%(tmp_ssf)
		exit(3) # not elegant

	for path in in_pathlist:
		of.write(path+'\r\n')

	of.close()

	fsslog = tmpdir+'/symstore-logfile.log'+retry_suffix

	# Call symstore.exe
	symstore_cmd = 'symstore add /o /f @%(scan)s /s %(dstore)s /t "%(product)s" /v "%(ver)s" /d "%(logfile)s"'%{
		"scan" : tmp_ssf ,
		"dstore" : g_dstore,
		"product" : g_prodn,
		"ver" : g_prodv,
		"logfile" : fsslog
		}
	try:
		print symstore_cmd
		subprocess.check_output(symstore_cmd, stderr=subprocess.STDOUT)
	except WindowsError:
		print "Error: symstore.exe not exist!"
		exit(4)
	except subprocess.CalledProcessError as cpe:
		print "Error: symstore execution fail, exit code is %d. Output is:\n%s"%(cpe.returncode , cpe.output)

	# Now, check symstore's logfile to get accurate result!
	# Rationale for success or fail: http://webs.dev.nls:8080/pages/viewpage.action?pageId=51740698
	ss_output = [] # to load symstore logfile lines
	oflog = open(fsslog, "r")
	if not oflog:
		print "Error: symstore.exe seems not generating a logfile at %s !"%(fsslog)
		exit(4)

	alllines = oflog.read()
	ss_output = alllines.split('\n')
	#ss_output = [line.strip() for line in alllines]
	oflog.close()

	# Check 1: the following lines(hint: at final several lines of output):
	"""
	SYMSTORE: Number of files stored = <actual-number>
	SYMSTORE: Number of errors = 0
	SYMSTORE: Number of files ignored = 0
	"""
	expect = r'SYMSTORE: Number of files stored = %d'%(len(in_pathlist))
	m = re.search(expect, alllines)
	if not m:
		print "Error: Cannot find '%s' in symstore output."%expect
		return -1, in_pathlist
	expect = r'SYMSTORE: Number of errors = 0'
	m = re.search(expect, alllines)
	if not m:
		print "Error: Cannot find '%s' in symstore output."%expect
		return -1, in_pathlist
	expect = r'SYMSTORE: Number of files ignored = 0'
	m = re.search(expect, alllines)
	if not m:
		print "Error: Cannot find '%s' in symstore output."%expect
		return -1, in_pathlist

	# Check 2: No ``error、fail、skip'' after every line of
	#	SYMSTORE MESSAGE: Copying <some-file> to <...>
	#
	# scan each line in ss_output[] to check matching of each input path:
	i = 0 # i is current line No.
	while i<len(ss_output):
		m = re.search(r'^SYMSTORE MESSAGE: Copying (.+) to', ss_output[i])
		if not m:
			i+=1
			continue
		ss_path = m.group(1) # find a matched path
		# Check next line for "error" or "fail" .
		err = False
		for errword in ['error', 'fail']:
			if ss_output[i+1].lower().find(errword)>=0 :
				err = True
				break
		if err:
			i+=2
			continue # ignore the failed one, go on searching matched path

		# good now, remove the matched path from in_pathlist
		try:
			in_pathlist.remove(ss_path)
		except ValueError: # Not likely to happen
			print "Unexpected: Line %d of %s reports path %s, but that path is not in %s."%(
				i+1, fsslog, ss_path, f_ssinput
				)
			exit(4)
		i+=1

	# Check 3: Extract symstore id from a line like
	#	SYMSTORE MESSAGE: Final id is 0000000011
	expect = r'SYMSTORE MESSAGE: Final id is ([0-9]+)'
	m = re.search(expect, alllines)
	if not m:
		print "Error: Cannot find regex '%s' in symstore output"%expect
		return -1, in_pathlist
	ss_finalid = m.group(1)

	return int(ss_finalid), in_pathlist


def DoStart():
	# Return an error code.

	# Walk our scan dir, generate a list of files to process(as symstore.exe's input-response-file)
	pickouts = [] # pick-out file list, including dir-scan prefix
	for root, folders, files in os.walk(g_dscan):
		# Filter through each pattern in gar_ptinc[]
		files_qualify = []
		for pt in gar_ptinc:
			files_qualify.extend(fnmatch.filter(files, pt))
		# Filter-out through each pattern in gar_ptexc[]
		files = files_qualify
		for pt in gar_ptexc:
			files = [f for f in files if not fnmatch.fnmatch(f, pt)]
		pickouts += [os.path.abspath(os.path.join(root, f)) for f in files]
		# Turn these paths into abspath is a must! because ``symstore /o'' will show abs path any way.
		# Sample symstore line:
		#
		#	SYMSTORE MESSAGE: Copying E:\temp\aq_pattern_match\make-sdk\sdk-msvc-all\nlssdk\vc80\lib\aq_pattern_match_D.lib.pdb to h:/temp/tssstore\aq_pattern_match_D.lib.pdb\58D6FA4540704316A6DCB5683EC64684\aq_pattern_match_D.lib.pdb [Force: T, Compress: F]
		#
		# --although the paths in ssinput.txt is relative path.
		# Storing abspath in ssinput.txt benefit us comparing our input path with symstore's feedback.

	npickout = len(pickouts)
	if npickout==0 :
		prompt = "Info: " if g_allow_empty_scan else "Error: "
		print prompt+"No matching files found. No files are pushed to symbol store."
		return 0 if g_allow_empty_scan else ErrNoFileProcessed

	ss_id_start, remain = CallSymstore_with_filelist(pickouts)
	ss_id_end = ss_id_start

	retry = 0
	while remain:
		retry+=1
		if retry>g_maxretry: break
		ss_id_end, remain = CallSymstore_with_filelist(remain, retry)

	if retry>g_maxretry :
		print "Error: %d/%d files cannot be symstored after %d retries."%(
			len(remain), npickout, g_maxretry
			)
		return 3
	else:
		print
		print "Success! %d files are symstored(%d retries). Resulting symstore IDs %d to %d."%(
			npickout, retry,
			ss_id_start, ss_id_end
			)
		return 0


def SetWildcardList(param):
	"""
	param is a string, sample:
		*.pdb/*.dll
	"""
	list = param.split('/')
	return list

def main():
	global opts, g_dscan, g_dstore, g_prodn, g_prodv, gar_ptinc, gar_ptexc
	global g_tmpdir, g_maxretry
	global g_allow_empty_scan

	reqopts = ['dir-scan=', 'dir-store=']
	optopts = ['3tier-symstore', 'pattern-include=', 'pattern-exclude=', 'tmpdir=', 'max-retry=', 
		'allow-empty-scan', 'version'] # optional arguments
	optlist,arglist = getopt.getopt(sys.argv[1:], '', reqopts+optopts)
	opts = dict(optlist)

	if '--version' in opts:
		print '%s v%s'%(os.path.basename(__file__), version)
		return 0

	if not AssertMissingOpt(reqopts, False):
		print "Options required:"
		print "    %s --dir-scan=<dirscan> --dir-store=<dirstore> [--3tier-symstore]"%(
			os.path.basename(__file__))
		return 1

	g_dscan = opts['--dir-scan']
	g_dstore = opts['--dir-store']
	
	if '--product-name' in opts:
		g_prodn = opts['--product-name']
	if '--product-ver' in opts:
		g_prodv = opts['--product-ver']

	if '--tmpdir' in opts:
		g_tmpdir = opts['--tmpdir']
	if '--max-retry' in opts:
		g_maxretry = opts['--max-retry']

	if '--pattern-include' in opts:
		gar_ptinc = SetWildcardList(opts['--pattern-include'])

	if '--pattern-exclude' in opts:
		gar_ptexc = SetWildcardList(opts['--pattern-exclude'])

	if '--allow-empty-scan' in opts:
		g_allow_empty_scan = True

	is_3tier = True if '--3tier-symstore' in opts else False

	# Assert valid directories
	for d in [g_dscan]:
		if not os.path.isdir(d):
			print "Error: Your input directory '%s' (abspath: %s) does not exist!"%(d, os.path.abspath(d))
			return 2

	# Assert creation of output directories
	for d in [g_dstore, g_tmpdir]:
		if os.path.isfile(d):
			print "Error: '%s' (abspath %s) is a file, not a directory!"%(d, os.path.abspath(d))
			return 2
		if not os.path.isdir(d):
			try:
				os.makedirs(d)
			except:
				print "Error: Cannot create symbol store directory '%s' (abspath: %s)!"%(d, os.path.abspath(d))
				return 2
	
	if os.listdir(g_dstore)==[] and is_3tier:
		p_index2txt = g_dstore+'/'+'index2.txt'
		try:
			open(p_index2txt, 'w').close()
		except IOError:
			print 'Error: Cannot create file "%s" for 3-tier symbol store.'%(p_index2txt)
			return 3

	err = DoStart()

	return err


if __name__ == '__main__':
	try:
		ret = main()
	finally:
		pass

	exit(ret)
