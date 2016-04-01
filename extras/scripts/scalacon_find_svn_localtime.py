#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
本程序为了解决这样一个问题：

当需要对一个本地目录中的 pdb 进行 PDB-sewing 时(实现于 scalacon-ssindex-svn.py)，如何选取 
--datetime-co 的值(dtco)，之前要手动指定，比较累人，现在要利用此程序自动确定 dtco 。

本程序扫描 --dirs-source 指明的一组本地目录(每个目录对应一个 svn sandbox，逗号分隔)，
来确定一个最终的 dtco 。操作步骤如下：

一, 检查所有 --dirs-source 指明的目录，确定不存在已修改但未提交的状态。

二，递归扫描所有沙箱目录，找出具有新时间戳的那个文件，将此时间戳往上取整秒，
	暂定其为 dtco (dtco_candidate)。 
	注意：是找出所有沙箱中最大时间戳，而非逐个沙箱确定最大时间戳。

三，比对沙箱当前状态 与 服务器在 dtco_candidate 时间点的状态(svn diff -r )，
	* 如果没有差异，则 dtco_candidate 即为最终确定的 dtco ，执行成功。
	* 如果有差异，说明本机的 PDB 跟 dtco_candidate 时的服务器内容是不匹配的，程序退出，宣告失败。

如果成功，将时间戳写出 stdout ，退出码为 0 。
如果失败，错误信息将写出 stderr 。

本程序通过 exit(error_text) 的方式来告知调用者执行失败，调用者捕获 SystemExit 来获知 error_text 。

或者：以编程方式调用 scalacon_find_svn_localtime() 来得到 svn datetime 字符串。

"""

import os
import re
import sys
import subprocess
import getopt
import time, datetime, calendar
import traceback

version = '1.2'

class SvnEntry: pass
	# 写到一半发现其实用不着收集所有各个 svn entry 的信息。用 svn diff -r <datetime> 就能进行
	# 本地文件跟服务器内容的差异判断。
	# 既然写了就先放着，今后可能有用。

def log_stderr(s):
	sys.stderr.write(s+"\n")

def svn_check_local_modification(rootdir):
	# Note: We use 'svn info' here because it fails a non-sandbox directory,
	# while 'svn status' does not report error, even for a non-existing directory.
	cmd = 'svn info ' + rootdir
	try:
		subprocess.check_output(cmd)
	except subprocess.CalledProcessError as cpe:
		exit('The directory "%s" is not an svn sandbox.'%s(rootdir))

	cmd = 'svn status -q ' + rootdir
	try:
		mls_modfiles = subprocess.check_output(cmd) # mls: multiline-string
	except subprocess.CalledProcessError as cpe:
		exit('Unexpected result executing "%s"'%(cmd))

	if mls_modfiles:
		return True
	else:
		# If no modifications found, stdout will be empty, and exit code is 0
		return False
		

def svn_find_latest_timestamp(rootdir, dentry):
	"""
	From all versioned-files in rootdir svn sandbox, find the latest timestamp,
	rounded up(123456789.5 rounded to 123456790) to Unix epoch seconds(in UTC).
	"""
	
	assert isinstance(dentry, dict)
		# Will fill dict with each svn local-file entry found in rootdir.
	
	cmd = 'svn status -v --xml ' + rootdir # This will automatically check sub-dirs.
	""" Output is something like:
<?xml version="1.0" encoding="UTF-8"?>
<status>
	<target path=".">

		<entry path=".">
			<wc-status item="normal" revision="285" props="none">
				<commit revision="285">
					<author>chj</author>
					<date>2016-04-01T02:17:58.954385Z</date>
				</commit>
			</wc-status>
		</entry>
		
		<entry path=".sdkbin-cache">
			<wc-status item="unversioned" props="none">
			</wc-status>
		</entry>
...
		<entry path="make\Makefile.umk">
			<wc-status item="normal" revision="285" props="none">
			<commit revision="281">
				<author>chj</author>
				<date>2016-03-31T09:23:03.416413Z</date>
			</commit>
			</wc-status>
		</entry>

	</target>
</status>
"""
	try:
		xml = subprocess.check_output(cmd)
	except subprocess.CalledProcessError as cpe:
		exit('The directory "%s" is not an svn sandbox.'%s(rootdir))

	max_revision = 1
	max_date = ''

	# Scan each <entry> to grab its <commit revision="nnn">'s nnn, store them for later comparison.
	for r in re.finditer(r'<entry\s+path="(.+?)">(.+?)</entry>', xml, re.DOTALL):
		entry_path = r.group(1)
		entry_content = r.group(2)
#		print "%s // %s"%(entry_path, entry_content) #debug
		# for each <entry> grab its commit revision
		r = re.search(
			r'<commit\s+revision="([0-9]+)">(?:.+?)<date>(.+?)</date>(?:.+?)</commit>', 
			entry_content, re.DOTALL)
		if r:
			entry_revision = r.group(1)
			date = r.group(2)
#			print "### %s (r=%s) date=%s"%(entry_path, entry_revision, date) #debug
			if entry_revision>max_revision:
				max_revision = entry_revision
				max_date = date 
			
			assert not entry_path in dentry
			dentry[entry_path] = SvnEntry()
			dentry[entry_path].rev = entry_revision
			
#	print "# %s entries collected in %s"%(len(dentry.keys()), rootdir) #debug
	
	epsec = svn_epsec_from_iso8601(max_date)
#	print "# %d"%(epsec)
	return epsec

def svn_epsec_from_iso8601(dt_str):
	# Thanks to: http://stackoverflow.com/a/127825/151453
    dt, _, us= dt_str.partition(".")
    dt= time.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    #us= int(us.rstrip("Z"), 10)
    #return dt + datetime.timedelta(microseconds=us)
    return calendar.timegm(dt)+1

def svn_update_to_epsec(rootdir, epsec):
	tm = gmtime(epsec)
	utc8601 = tm.strftime("%Y-%m-%dT%H:%M:%SZ")
	cmd = 'svn update -r {%s} %s'%(utc8601, rootdir)
	print ">>> Running: %s"%(cmd)
	try:
		subprocess.check_output(cmd)
	except subprocess.CalledProcessError as cpe:
		exit('Unexpected result executing: "%s"'%s(cmd))

def svn_diff_timestamp(rootdir, epsec):
	tm = time.gmtime(epsec)
	utc8601 = time.strftime("%Y-%m-%dT%H:%M:%SZ", tm)
	cmd = 'svn diff --summarize --xml -r {%s} "%s"'%(utc8601, rootdir)
	try:
		xml = subprocess.check_output(cmd)
	except subprocess.CalledProcessError as cpe:
		exit('Unexpected result executing: %s'%s(cmd))

	"""
If no difference found, output is:

<?xml version="1.0" encoding="UTF-8"?>
<diff>
<paths>
</paths>
</diff>

If difference found, output is like:

<?xml version="1.0" encoding="UTF-8"?>
<diff>
<paths>
<path props="none" kind="file" item="modified">KeyView2.vcxproj</path>
<path item="modified" props="none" kind="file">get-sdkin.ini</path>
<path item="modified" props="none" kind="file">KeyView2.cpp</path>
<path
   props="none"
   kind="file"
   item="deleted">desktop.ini</path>
</paths>
</diff>
"""
	changed_files = []
	for r in re.finditer(r'<path\s+(?:.+?)>(.+?)</path>', xml, re.DOTALL):
		changed_files.append(r.group(1))
	
	return changed_files

def svn_timezone_string():
	tzsec = time.timezone
	if tzsec<=0:
		tzsec = -tzsec
		# east of UTC, 
		s = '+%02d%02d'%(tzsec/3600, tzsec/60%60) 
			# China is '+0800'
	else:
		# west of UTC
		s = '-%02d%02d'%(tzsec/3600, tzsec/60%60) 
	
	return s

def scalacon_find_svn_localtime(dirs_source):
	# Check that there is no local sandbox modification.
	for rootdir in dirs_source:
		if svn_check_local_modification(rootdir):
			exit('Your sandbox "%s" has local modifications.'%(rootdir))
	
	sandboxes = {}
		# sandboxes['D:/w/myproj'] is again a dict.
		# sandboxes['D:/w/myproj']['file1.cpp'] is an SvnEntry object describing file1.cpp's property
	
	# Find the latest svn-versioned file in all dirs_source.
	epsec_latest = 0
	for rootdir in dirs_source:
		sandboxes[rootdir] = {}
		epsec = svn_find_latest_timestamp(rootdir, sandboxes[rootdir])
		if epsec>epsec_latest:
			epsec_latest = epsec

	tmlocal = time.localtime(epsec_latest)
	timestrlocal = time.strftime('%Y-%m-%d %H:%M:%S', tmlocal)

	# Check whether sandbox content matches server's at epsec_latest time point.
	for rootdir in dirs_source:
		changed_files = svn_diff_timestamp(rootdir, epsec)
		if changed_files:
			errmsg = 'The latest files in your sandboxes has (local) timestamp %s, '\
			'but local content does not exactly match server content.\n'\
				'Different files are:\n  %s'%(timestrlocal, '\n  '.join(changed_files))
			exit(errmsg)
	
	ret = timestrlocal +' '+ svn_timezone_string()
	return ret
	

if __name__ == '__main__':
	dirs_source = [os.path.abspath(dir) for dir in sys.argv[1].split(',')]
	try:
		ret = scalacon_find_svn_localtime(dirs_source)
		print 'Determined svn datetime is: %s'%(ret)
	except SystemExit as e:
		log_stderr(e.code) # e.code is the error string from exit().
		exit(4)
	except:
		exc_string = traceback.format_exc()
		log_stderr(exc_string)
		exit(5)

	exit(0)
	



