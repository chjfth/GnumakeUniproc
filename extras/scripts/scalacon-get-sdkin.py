#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取一个或多个外来的 SDK 二进制文件到本地，成为本地 SDK 。

--ini=<ini-filepath>
	[必须] 描述外来 SDK 的 ini 文件。

--use-svn-checkout
	[可选] 
	使用 svn checkout 而非 svn export 来抓取服务器内容。
	checkout 比 export 会消耗多一倍的磁盘空间，但好处在于中途发生网络中断后可以
	svn cleanup 后续传。

--force
	[可选]
	强制模式。意思是，对于每一条外来 SDK 描述，先将其指示的本地目录清空。
	所有本地目录条目都清空后，再从各条 SDK 的 svnurl 抓取内容，以此保证
	本地目录中不存在已废弃的文件。
	.
	如果不用 --force, 则不作任何清空动作，且，处理每一个 SDK 条目时，若
	本地目录已经存在（不管里面的内容如何）就跳过服务端抓取动作。
	.
	--force 同时暗示非交互操作。

--self=[<dir-sdkout>]
	[可选]
	仅取 [self] 小节的内容。不指定则只会取其他小节(sdkin)的内容。
	本选项的值指出将 self 内容取到哪个本地目录中（覆盖 gmb_dirname_sdkout）。
	如果 = 后是空值，则 localdir 仍旧遵照 INI 中的描述。

--get-all
	[可选]
	取 sdkin 和 sdkout 。即使用了 --self ， --get-all 也生效。

--sdkbin-limit=<filter1>,<filter2>
	[可选]
	限定仅取特定的某些 refname （不需要 sdkin. 和 self. 前缀）。
	用途： INI 中有两个小节 [sdkin.foo-vc100] [sdkin.foo-vc100x64] ，默认会全取这两个小节。
	但如果某个用户工程只想编 64-bit 的程序，那么他可以在 get-sdkin.bat 中指定(任一种):
		--sdkbin-limit=foo-vc100x64 
		--sdkbin-limit=x64
		--sdkbin-limit=*x64
	来只取 [sdkin.foo-vc100x64] 小节指定的内容。
	在 --force 操作时可以用此选项挑出部分 sdk refname 来更新。
	
--simulate
	[可选]
	模拟网络失败的情况。此选项供本程序开发者调试用。

=== >>> INI 格式范例

[DEFAULT]
NLSSVN=https://nlssvn.dev.nls/svnreps
gmb_dirname_sdkin=sdkin
gmb_dirname_sdkout=sdkout

cidvers_restrict=

[sdkin.common-include]
svndatetime= 2016-03-05 23:00
svnurl=      %(NLSSVN)s/CommonLib/common-include/trunk
localdir=    %(gmb_dirname_sdkin)s/include
; -- localdir is relative to this INI file.
implicit-cidver-mapping=
explicit-cidver-mapping=

[sdkin.mm_snprintf]
svndatetime= 2016-03-06 13:39:43
svnurl=      %(NLSSVN)s/scalacon/sdkbin/mmsnprintf/4.2.0
localdir=    %(gmb_dirname_sdkin)s

[self.IUartBasic]
svndatetime= 2016-03-11 11:44:00
svnurl=      %(NLSSVN)s/scalacon/sdkbin/IUartBasic/2.1.6
localdir=    %(gmb_dirname_sdkout)s

=== <<< INI 格式范例

[DEFAULT] 小节用来定义一些全局变量的默认值，以便稍后多次引用。

[DEFAULT] 中定义的条目会被同名环境变量覆盖，这个覆盖动作是在本 .py 代码中实现的。

	cidvers_restrict=<cidvers list>    (可选)
	
	例：
	cidvers_restrict=vc100 vc100x64 
		只在 $/sdkin, $/sdkout 中生成 vc100 的二进制。
		换言之， $/sdkbin-cache 中还是会取到 svn 上的全部 cidvers ，但只将 vc100 和 vc100x64 
		的二进制拷贝到 $/sdkin, $/sdkout 中。
	
	环境变量中设置 cidvers_restrict=0 ，用于覆盖 INI 中的 cidvers_restrict 设定，
	相当于临时解除了 cidvers 限制。
	设计 =0 的原因：由于无法创建一个“空值”的环境变量，因此，想把 INI 中的 cidvers_restrict
	覆盖成空值，只能作个特殊规定。

[self.xxx] 小节，指示自己这个 SDK 的最新发布包，该内容默认将被取出到 sdkout 子目录中。
[self.xxx] 小节的内容仅仅在传递了 --self 时才会去获取。注意，进行 make-sdk-all 构建后，
sdkout 子目录中的内容会被覆盖（除非 make-sdk-all 选取不同的 SDK output 目录）。
可以有多个 self. 小节来指示 self 来自多处，比如，将 [self.Windows] 和 [self.Linux] 。


其他的小节，若小节名以 sdkin. 起始，则此小节对应一个 SDK 条目，sdkin. 后的子串
可以任意命名，跟 SDK 本身并无相关性。

svndatetime 
	指出抓取 svn 仓库中哪个时间点的内容，将用作 svn export 的 peg 参数。
	
svnurl 
	指出 SVN 服务端地址。

localdir 
	指出跟 svnurl 对应的本地目录。
	对照以上范例， https://nlssvn/svnreps/CommonLib/common-include/trunk/ps_TCHAR.h 
	将对应本地文件 $/sdkin/include/ps_TCHAR.h 
	（此句用 $ 代表此 INI 所在的目录）
	注意 sdkin 实际上由环境变量 gmb_dirname_sdkin 控制。

额外行为：

【cidver-mapping】 对于一个小节，在 want-cidver-mapping=1 的情况下，启动 cidver-mapping 行为。

cidver 是指 vc60, vc80, vc100x64, gcc4.8_i686 这样的字眼，不同的 cidver 意味着用户可以使用
不同版本的编译器来构建自己的工程。 一个 cidver 将呈现为 $/sdkin 中的一个子目录名。

$/sdkin 中最终呈现的 cidver ，以及 cidver 中的内容由四层信息叠加而成。

(1) 输入库(SDKIN)提供的实质 cidver 。比如，某个输入库有用 vc80 进行编译，则它实质提供 vc80 。
(2) 输入库自带的 cidver-mapping.ini 指示的映射所产出的 cidver 。
(3) 库用户自身 get-sdkin.ini 中 implicit-cidver-mapping= 指示的隐式映射。隐式的意思是，
	当 (1)(2) 没有提供所需的 cidver 时，隐式映射起作用。
(4) 库用户自身 get-sdkin.ini 中 explicit-cidver-mapping= 指示的强制映射。强制的意思是，
	覆盖掉 (2),(3) 的映射方法，直接建立跟 (1) 的映射关系。若 (1) 中没有期望的 cidver 目标，
	宣告失败。

im/explicit-cidver-mapping= 的取值格式：

implicit-cidver-mapping = vc100(=vc80) vc100x64(=vc80x64)

当 want-cid-mapping=1 时，implicit-cidver-mapping= 和 explicit-cidver-mapping= 可以为空，表示
仅仅遵循第 (2) 层的 mapping 。

——实现于 get_cidvers_mapping_dsuo(), get_cidvers_reverse_mapping_dsuo()

"""

import os
import sys
import time
import getopt
import subprocess
import shlex
import shutil
import stat
import ConfigParser # INI op
import re
import fnmatch
from distutils.version import LooseVersion, StrictVersion

version = "1.4"
optdict = {}
g_ini_filepath = '' # the config file(in INI format)
g_ini_dir = ''
g_isforce = False
g_is_do_self = False
g_is_only_self = False
g_self_dir_param = ''

g_is_svn_checkout = False

g_cidvers_restrict = []

g_sdkbin_limits = []

g_is_simulate = False

DIRNAME_CACHE = '.sdkbin-cache'

FN_CIDVER_MAPPING = 'cidver-mapping.ini'
FN_CACHED_GET_SDKIN_INI = 'user-sdkin.ini' 
	# A copy of user's get-sdkin.ini in each sdk_refname directory. 
	# I use different name for FN_CACHED_GET_SDKIN_INI just for easier explanation.
FN_SVNDATETIME_CKT = 'svndatetime.ckt.txt'
FN_PATTERN_REFNAME_DONE = 'refname.%s.done.txt'

SUFFIX_NEW = '.new'
SUFFIX_OLD = '.old'

# IK_ INI key name:
IK_svndatetime = 'svndatetime'
IK_svnurl = 'svnurl'
IK_localdir = 'localdir'
IK_comment = 'comment'

g_required_subdir_in_sdkin = ['include', 'cidvers' ]

class GetsdkError(Exception):
	def __init__(self, errmsg):
		self.errmsg = errmsg
	def __str__(self):
		return self.errmsg


def cachedirs(sdk_refname):
	assert os.path.isabs(g_ini_dir)
	dir_sdkcache = os.path.join(g_ini_dir, DIRNAME_CACHE)
	refname_cache = os.path.join(dir_sdkcache, sdk_refname)
	return dir_sdkcache, refname_cache, refname_cache+SUFFIX_NEW

def is_A_older_than_B(fileA, fileB):
	# A(mlocal_sigfile) is consider older if not exist.
	assert os.path.exists(fileB)
	if not os.path.exists(fileA):
		return True

	Atime = int( os.path.getmtime(fileA) )
	Btime = int( os.path.getmtime(fileB) )
	return True if Atime<Btime else False
	

def os_sep(hint=""):
	# A more friendly os.sep .
	fs_pos = hint.find('/')
	bs_pos = hint.find('\\')
	if fs_pos<0 and bs_pos<0:
		return os.sep
	elif fs_pos<0: # forward slash not found, so there is a backslash
		return '\\'
	elif bs_pos<0:
		return '/'
	else:
		return '/' if fs_pos<bs_pos else '\\'
		
def os_sep_unify(path):
	if os_sep(path)=='/':
		return path.replace('\\', '/')
	else:
		return path.replace('/', '\\')

def rmdir_if_empty(dir):
	# The logic below is not scrupulous, only just works for Scalacon.
	def can_ignore(dir, entry):
		abs_entry = os.path.join(dir, entry)
		if os.path.isdir(abs_entry):
			return False
#		elif fnmatch.fnmatch(entry, '_*.txt'):
			return True
		elif os.path.getsize(abs_entry)==0:
			return True
		else:
			return False
	
	entries = os.listdir(dir)
#	print "@@@ Check removing dir %s"%(dir) , #debug
#	if dir.find('VC80__'): print "  ---%s"%(entries) #debug
	
	keep = False
	for entry in entries:
		if not can_ignore(dir, entry):
			keep = True
			break
		
#	print "[keep]" if keep else '[REMOVE]' #debug
	if not keep:
		force_rmtree(dir)

def os_remove_easy(filepath, is_remove_empty_dir=False):
	if os.path.exists(filepath):
		os.chmod(filepath, stat.S_IWRITE)
	try:
		os.remove(filepath)
	except OSError:
		if os.path.exists(filepath):
			raise
		else:
			pass
	
	if is_remove_empty_dir:
		dir = os.path.split(filepath)[0]
		rmdir_if_empty(dir)
	

def force_rmtree(dir):
	# Remove read-only attribute for files inside.
	for root, dirs, files in os.walk(dir):
		for file in files:
			os.chmod(root+'/'+file, stat.S_IWRITE)

	# Then remove the whole tree.
	if os.path.isdir(dir):
		shutil.rmtree(dir)

def force_copyfile(src, dst):
	if os.path.exists(dst):
		os.chmod(dst, stat.S_IWRITE)
	
	shutil.copyfile(src, dst)
	shutil.copystat(src, dst) 
		# let them have the same modification time, so that later when 
		# syncing $/sdk-cache to $/sdk, we can know whether a file in $/sdk 
		# has local modification.
	
	
def copytree_overwrite(src, dest, ignore=None):
	# Thanks to: http://stackoverflow.com/a/15824216/151453
	if os.path.isdir(src):
		if not os.path.isdir(dest):
			try:
				os.makedirs(dest)
			except OSError:
				if not os.path.isdir(dest):
					raise
		files = os.listdir(src)
		if ignore is not None:
			ignored = ignore(src, files)
		else:
			ignored = set()
		for f in files:
			if f not in ignored:
				copytree_overwrite(os.path.join(src, f), 
									os.path.join(dest, f), 
									ignore)
	else:
		force_copyfile(src, dest)


def enume_sections(iniobj, g_ini_dir):
	sdknames = iniobj.sections()
	for section in sdknames:
		if section.startswith('self.') and not g_is_do_self:
			continue
		if (not section.startswith('self.')) and g_is_only_self:
			continue
		
		if section.startswith('sdkin.'):
			sdk_refname = re.sub(r'^sdkin\.', '', section)
		elif section.startswith('self.'):
			sdk_refname = re.sub(r'^self\.', '', section)
		else:
			print "Scalacon info: Ignoring unrecognized section name [%s]."%(section)
			continue # unrecognized section name
		
		kvlist = iniobj.items(section)
		dsection = dict(kvlist)
		if not 'localdir' in dsection:
			dsection['localdir'] = '.'
		
		if section=='self':
			localdir = g_self_dir_param if g_self_dir_param else dsection['localdir']
		else:
			localdir = dsection['localdir']
		
		localdir_final = os.path.abspath( os.path.join(g_ini_dir, localdir) )
		yield section, dsection, sdk_refname, localdir_final # dsection's d implies dict


def merge_sdk_self_mapping(mapping, inifile):
	# [in/out] mapping
	# Grab a cidver-mapping.ini from your harddisk to know the format of this inifile.
	"""Sample: 
[mapping]
vc90=vc80
vc90x64=vc80x64
...
"""
	#
	iniobj = ConfigParser.ConfigParser()
	iniobj.read(inifile)
	kvpairs = iniobj.items('mapping')
	for virtual, real in kvpairs:
		mapping.setdefault(virtual, [])
		mapping[virtual].insert(0, real)
	

def make_cidver_mapping_dict(mapping_spec):
	d = {}
	mapping_entries = mapping_spec.split()
	for entry in mapping_entries:
		# one entry is like: "vc100(=vc80)"
		r = re.match(r'(.+)\(=(.+)\)' , entry)
		if not r or not len(r.groups())==2:
			print 'Scalacon Error: %s contains invalid cidver mapping spec: "%s"'%(g_ini_filepath, entry)
			exit(24)
		virtual_cidver = r.group(1)
		real_cidver = r.group(2)
		d[virtual_cidver] = real_cidver
		
	return d

def get_cidvers_mapping(cidvers_dir, self_mapping_ini, user_override_ini, user_section):
	iniobj = ConfigParser.ConfigParser()
	okini = iniobj.read(user_override_ini)
	assert okini # ensure the ini file exists

	kvlist = iniobj.items(user_section)
	dsection = dict(kvlist)
	
	return get_cidvers_mapping_dsuo(cidvers_dir, self_mapping_ini, dsection)


def get_cidvers_mapping_dsuo(cidvers_dir, self_mapping_ini, dsection_user_override):
	"""
	_dsuo: implies dsection_user_override
	
	cidvers_dir: (layer 1)
		The dir that contains actual vc60, vc80 cidver-subdirs.
		Example: 
			$/sdkbin-cache/common-include/cidvers
			$/sdkbin-cache/mm-snprintf/cidvers
	
	self_mapping_ini: (layer 2)
		Example:
			$/sdkbin-cache/common-include/cidver-mapping.ini
			$/sdkbin-cache/mm-snprintf/cidver-mapping.ini
	
	dsection_user_override: (layer 3,4)
		The INI section(in dict form) describing SDK user cidver-mapping override.
	
	Return:
		Mapping information(in dict form) from real cidver to virtual cidver. 
		i.e. mapping[virtual]=[ real1, real2, ...]
		
		Example: 
			mapping['vc100']=['vc90', 'vc80']
		means:
		SDK-user's vc100 will be mapped to vc90; some previous layer has mapped it to 'vc80' but has been overridden.
		I record the overridden info just for debugging purpose.
	"""

	mapping = {}

	# layer 1: real <cidver> folder, vc60, vc80 etc 
	list_cidvers = os.listdir(cidvers_dir)
	assert list_cidvers
	for cidver in list_cidvers:
		mapping[cidver] = [cidver]
	
	# layer 2: cidver-mapping.ini
	if os.path.isfile(self_mapping_ini):
		merge_sdk_self_mapping(mapping, self_mapping_ini)
	
	# layer 3: SDK-user implicit mapping
	implicit_mapping_spec = dsection_user_override['implicit-cidver-mapping'] \
		if 'implicit-cidver-mapping' in dsection_user_override \
		else ''
	explicit_mapping_spec = dsection_user_override['explicit-cidver-mapping'] \
		if 'explicit-cidver-mapping' in dsection_user_override \
		else ''
	
	if implicit_mapping_spec:
		implicit_mapping_dict = make_cidver_mapping_dict(implicit_mapping_spec)
		for virtual_cidver in implicit_mapping_dict.keys():
			# add this mapping only in case of NOT exist (i.e. implicit)
			if not virtual_cidver in mapping: 
				mapping[virtual_cidver] = [ implicit_mapping_dict[virtual_cidver] ]
	
	# layer 4: SDK-user explicit mapping
	if explicit_mapping_spec:
		explicit_mapping_dict = make_cidver_mapping_dict(explicit_mapping_spec)
		for virtual_cidver in explicit_mapping_dict.keys():
			# always use this mapping(explicit)
			mapping.setdefault(virtual_cidver, [])
			mapping[virtual_cidver].insert(0, explicit_mapping_dict[virtual_cidver])

	return mapping

def get_cidvers_reverse_mapping(cidvers_dir, self_mapping_ini, user_override_ini, user_section):
	dsection_user_override = {}
	iniobj = ConfigParser.ConfigParser()
	okini = iniobj.read(user_override_ini)
	
	if okini:
		kvlist = iniobj.items(user_section)
		dsection_user_override = dict(kvlist)

	rmapping = get_cidvers_reverse_mapping_dsuo(cidvers_dir, self_mapping_ini, dsection_user_override)
	return rmapping

def get_cidvers_reverse_mapping_dsuo(cidvers_dir, self_mapping_ini, dsection_user_override):
	mapping = get_cidvers_mapping_dsuo(cidvers_dir, self_mapping_ini, dsection_user_override)

	rmapping = {}
		# Result: 
		#	rmapping[real] = [virtual1, virtual2]
		# Result Sample:
		#	rmapping['vc100'] = ['vc100', 'vc120', 'vc140'] # order does not matter
	
	for vcidver in mapping:
		real_cidver = mapping[vcidver][0]
		rmapping.setdefault( real_cidver, [] )
		rmapping[real_cidver].append(vcidver)
	
	return rmapping
	

def check_cidver_case_correct(dir, cidver):
	# Assert that cidver has the matching upper/lower case as that in dir(file system directory).
	entries = os.listdir(dir)
	is_ok = True if cidver in entries else False
	correct_case = None
	for entry in entries:
		if entry.lower()==cidver.lower():
			correct_case = entry
			break
	return is_ok, correct_case

def sync_sdkcache_to_sdklocal(section, dsection, sdk_refname, localdir):
	# section is INI section name,
	# im/explicit_mapping_spec sample: "vc100(=vc80) vc100x64(=vc80x64)"

	dir_sdkcache, dir_refname = cachedirs(sdk_refname)[:2]
	
	# Apply four-layer cid-mapping:
	cidvers_dir = os.path.join(dir_refname, 'cidvers')
		# cidvers_dir is expected to contain sub-dirs like vc60, vc80, vc100x64 etc
	self_mapping_ini = os.path.join(dir_refname, FN_CIDVER_MAPPING)

	mapping = get_cidvers_mapping_dsuo(cidvers_dir, self_mapping_ini, dsection)

	# Do our sync(copy) work according to mapping:
	
	for subdir in g_required_subdir_in_sdkin:
		if subdir=='cidvers':
			continue # cidvers\vc60, cidvers\vc80 etc will be copied later with special action
		print '  Storing subdir "%s"'%(subdir)
		copytree_overwrite(
			os.path.join(dir_refname, subdir),
			os.path.join(localdir, subdir))

	# Now, generate virtual cidver dirs(directly in localdir) by copying from their real bodies
	skips = []
	count = 0
	ordered_vcidvers = sorted(mapping.keys())
	if ordered_vcidvers:
		print '  Storing subdir "cidvers":'
	for virtual_cidver in ordered_vcidvers:
		
		if g_cidvers_restrict:
		    if not [ptn for ptn in g_cidvers_restrict if fnmatch.fnmatch(virtual_cidver, ptn)]:
				skips.append(virtual_cidver)
				continue
		
		real_cidver = mapping[virtual_cidver][0]
		dir_src = os.path.join(dir_refname, 'cidvers', real_cidver)
		dir_dst = os.path.join(localdir, 'cidvers', virtual_cidver)
		
		if not os.path.isdir(dir_src):
			# try link layer(3-4) to layer 2 (just one more level of mapping)
			if not real_cidver in mapping:
				print 'Scalacon Error: You request mapping "%s" to real cidver "%s" but the directory "%s" does not exist(cidver upper/lower case matter), '\
					'which means that input SDK(INI section [%s]) does not provide that cidver.'%(
					virtual_cidver, real_cidver, dir_src, section)
				exit(25)
			real_cidver = mapping[real_cidver][0]
			dir_src = os.path.join(dir_refname, 'cidvers', real_cidver)
			assert os.path.isdir(dir_src)
		
		is_ok, correct_case = check_cidver_case_correct( *os.path.split(dir_src) )
		if not is_ok:
			assert correct_case
			print 'Scalacon Error: You assign real cidver "%s" in INI section [%s], but the upper/lower case is not correct. ' \
				'The correct case is %s .'%(real_cidver, section, correct_case)
			exit(26)
		
		count += 1
		count_show = ('(%d)'%(count)).ljust(4)
		if virtual_cidver == real_cidver:
			print '  %s Storing <%s>'%(count_show, virtual_cidver)
		else:
			print '  %s Storing <%s> from %s'%(count_show, virtual_cidver, real_cidver)
		
		copytree_overwrite(dir_src, dir_dst)
		
		# create an empty file telling user the cidver's real body
		if virtual_cidver != real_cidver:
			filename_cidver_source_hint = "_[%s]CopiedFromCidver.%s.txt"%(section, real_cidver)
			open(os.path.join(dir_dst, filename_cidver_source_hint), "wb").close()
	
	if skips:
		print '  Skipped cidvers: %s'%(', '.join(skips))
	
	# Create FN_PATTERN_REFNAME_DONE signature file in localdir.
	fp_refname_done = os.path.join(localdir, FN_PATTERN_REFNAME_DONE%(sdk_refname))
	open(fp_refname_done, 'wb') # yes, create an empty file
	
	# Generate in dir_refname a copy of FN_CACHED_GET_SDKIN_INI, for later remove-old-file's correct cidver-mapping behavior. 
	inipath_copy = os.path.join( dir_refname, FN_CACHED_GET_SDKIN_INI )
	shutil.copyfile(g_ini_filepath, inipath_copy)
	

def cache_to_local_enum_pair(section, dsection, dir_refname, localdir):
	"""
	This is a generator. It outputs pairs (psrc, pdst):
	psrc is a filepath or dirpath inside $/.sdkin-cache 
	pdst is a filepath or dirpath inside $/.sdkin 
	The pdst are actually a copy from psrc; the copy was done in previous scalacon-get-sdkin.py run.
	"""
	
	if not os.path.exists(dir_refname):
		return
	
	inipath_cidver_mapping = os.path.join(dir_refname, FN_CIDVER_MAPPING)
	cidvers_dir = os.path.join(dir_refname, 'cidvers')
	old_user_getsdkini = os.path.join(dir_refname, FN_CACHED_GET_SDKIN_INI)
	rmapping = get_cidvers_reverse_mapping(cidvers_dir, inipath_cidver_mapping, old_user_getsdkini, section)
	# print "### rmapping:", rmapping #debug
		# Sample return( rmapping[real]=virtual ):
		# rmapping['vc100'] = ['vc100', 'vc120', 'vc140'] # the list will include 'vc100' itself
		# -- which means: virtual cidver(vcidver) vc120 and vc140 are both mapped to real cidver vc100
	
	# We walk the dir in two passes, first excluding the cidvers dir, second for the cidvers dir,
	# because cidvers dir is special(need cidver-mapping process).
	#
	# Memo: contents in dir_refname corresponds to contents in localdir.
	# Memo: use topdown=False in os.walk below, so that "empty-directory removing" works 
	# in clean_old_local_by_old_refname().

	# pass1:
	pass1_roots = filter(lambda x:x!='cidvers', g_required_subdir_in_sdkin)
	for rootname in pass1_roots: # root implies walk-root
		proot = os.path.join(dir_refname, rootname) # p:path
			# Example: proot=r'D:\myproj\.sdkbin-cache\mm_snprintf\include'
		for dirpath, dirnames, files in os.walk(proot, topdown=False):
			for entry in files+dirnames:
				psrc = os.path.join(dirpath, entry)
				pdst = os.path.join(localdir, psrc[len(dir_refname):], entry)
				yield psrc, pdst
		yield proot, os.path.join(localdir, rootname)
			
	# pass2:
	srcdir_cidvers = os.path.join(dir_refname, 'cidvers')
	pass2_roots = filter( lambda x:os.path.isdir(os.path.join(srcdir_cidvers,x)), os.listdir(srcdir_cidvers) )
	for real_cidver in pass2_roots: # root implies walk-root, real_cidver is like vc60, vc80, vc100 etc
		proot = os.path.join(srcdir_cidvers, real_cidver)
			# Example: proot = D:\myproj\.sdkbin-cache\mm_snprintf\cidvers\vc100
		for dirpath, dirnames, files in os.walk(proot, topdown=False): 
			for entry in files+dirnames:
				psrc = os.path.join(dirpath, entry)
				midpart = os.path.split(psrc[len(proot)+1:])[0] # +1 is for the '\' after proot
					# Example: If current 
					# psrc is 
					#	D:\myproj\.sdkbin-cache\mm_snprintf\cidvers\vc100\bin-debug\foo.dll
					# Localdir is 
					#	D:\myproj\sdkbin
					# then the corresponding virtual entry may be:
					#	D:\myproj\sdkbin\cidvers\vc120\bin-debug\foo.dll
					# or
					#	D:\myproj\sdkbin\cidvers\vc140\bin-debug\foo.dll
					# so the midpart is:
					#	bin-debug
					#
					# -- Note: midpart may be empty, which is OK.
				for vcidver in rmapping[real_cidver]:
					pdst = os.path.join(localdir, 'cidvers', vcidver, midpart, entry)
					yield psrc, pdst
		for vcidver in rmapping[real_cidver]:
			yield proot, os.path.join(localdir, 'cidvers', vcidver)
	

def fetch_sdkcache_1refname(section, dsection, sdk_refname, localdir):
	svnurl = dsection['svnurl']
	ini_svndatetime = dsection['svndatetime']
	
	# 此函数的工作是：
	# 1. 先将 svn 抓取的内容存放在 $/sdkbin-cache/gadgetlib.new 目录中，
	#    抓取成功后在其中创建 svndatetime.ckt.txt 记录同步时间戳。
	# 2. 改名 $/sdkbin-cache/gadgetlib 为 $/sdkbin-cache.old 。
	# 3. $/sdkbin-cache/gadgetlib.new 改名为 $/sdkbin-cache/gadgetlib 。
	# 此时需要留着 .old 目录的目的是：稍后需要根据 .old 中的信息来删除 $/sdkin 中的老内容。
	# （包括删除掉被 cidver-mapping 生成的老文件)

	# 先判断 $/sdkbin-cache/gadgetlib.new 中的同步时间戳是否匹配 INI 的，是的话说明上回已抓取成功过，
	# 此目录中的内容是有效的，此回就不用再去 svn 抓取了(即跳过 step 1)。

	dir_sdkcache, dir_refname, dir_refname_new = cachedirs(sdk_refname)
		# Sample: dir_sdkcache=$/sdkbin-cache , dir_refname=$/sdkbin-cache/gadgetlib

	fp_svndatetime_tmp = os.path.join(dir_refname_new, FN_SVNDATETIME_CKT)
	fp_svndatetime = os.path.join(dir_refname, FN_SVNDATETIME_CKT)
	try:
		tmp_svndatetime = open(fp_svndatetime_tmp, 'rb').read()
	except IOError:
		tmp_svndatetime = 'none'

	# step 1.
	if tmp_svndatetime != ini_svndatetime:
		# Grab svn server content into .new folder first.
		svncmd = 'svn %s --force "%s@{%s}" "%s"'%( 
			'checkout' if g_is_svn_checkout else 'export',
			svnurl, ini_svndatetime, dir_refname_new
			)
		print "Running cmd: \n  " + svncmd
		
		sys.stdout.flush(); 
			# [2016-03-31] Special Note: I have to flush stdout before calling svn.exe child process.
			# Without this flush, when piping the screen output to tee, I see "svn export"'s output 
			# come out BEFORE the print content above.
	
		if g_is_simulate:
			raise GetsdkError('[Simulate] Network failure on svn command: %s'%(svncmd))
		else:
			ret = subprocess.check_call(shlex.split(svncmd))
		
		open(fp_svndatetime_tmp, 'wb').write(ini_svndatetime)

	# step 2.
	dir_refname_old =  dir_refname+SUFFIX_OLD
	if os.path.exists(dir_refname_old):
		clean_old_local_by_old_refname(section, dsection, dir_refname_old, localdir, True)
	
	if os.path.exists(dir_refname):
		os.rename(dir_refname, dir_refname_old)
	
	# step 3.
	os.rename(dir_refname_new, dir_refname)

def check_cached_svndatetime_1refname(dsection, sdk_refname):
	dir_sdkcache, dircache_this_refname = cachedirs(sdk_refname)[:2]
	fp_svndatetime_cache = os.path.join(dircache_this_refname, FN_SVNDATETIME_CKT)
	try:
		cached_svndatetime = open(fp_svndatetime_cache, 'rb').read()
	except IOError: # the file fp_svndatetime_cache not exist
		return 'not_exist'
	
#	if dsection[IK_svndatetime] == cached_svndatetime:
#		return cached_svndatetime
#	else:
#		return cached_svndatetime
	return cached_svndatetime

def get_mlocal_sigfile_1refname(localdir, sdk_refname):
	# mlocal: merged local
	fn_sdkin_done_chk = FN_PATTERN_REFNAME_DONE%(sdk_refname)
	fp_sdkin_done_chk = os.path.join(localdir, fn_sdkin_done_chk)
	return fp_sdkin_done_chk

def check_mlocal_exist_1refname(localdir, sdk_refname):
	if os.path.exists( get_mlocal_sigfile_1refname(localdir, sdk_refname) ):
		return True
	else:
		return False


def clean_old_local_by_old_refname(section, dsection, dir_refname_old, localdir, is_remove_old):
	# 根据原 $/sdkbin-cache/gadgetlib 中的文件 对应着 删除 $/sdkin 中的同名文件（用于消除已废弃的文件）。
	# 此中同时进行了 cidver mapping 处理，即，将原先因为 cidver-mapping 而得的文件也一并删除。
	#
	# We use the existence of the <refname>.old directory as "transaction signature".
	
	# Note: dir_refname_old may end in ".old" or not, according to calling context.
	
	if not os.path.exists( dir_refname_old ):
		return True # go on sync
	
	print '[%s]Removing old files in localdir ...'%(section)
	
	if not g_isforce: # force means direct-overwrite target, "not force" means ask bfr overwrite
		# Check for file modification in localdir(e.g. user dropped in a trial-built binary).
		# If any modification is found, let user determine whether to overwrite them.
		count = 0
		for fp_src, fp_dst in cache_to_local_enum_pair(section, dsection, dir_refname_old, localdir):
			if not os.path.exists(fp_dst):
				continue
			
			if os.path.isdir(fp_dst):
				continue # no sense to compare directory time
				
			srctime = int( os.path.getmtime(fp_src) )
			dsttime = int( os.path.getmtime(fp_dst) )
			if srctime != dsttime:
				count += 1
				print "Found %d target file with local modification(different timestamp):"%(count)
				print "  Cached (%s): %s"%( 
					time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(srctime)), fp_src)
				print "  Target (%s): %s"%(
					time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dsttime)), fp_dst)
		
		if count>0:
			a = raw_input("[%s]Shall I overwrite/remove those target files?[Y/n] "%(section))
			if not (a in ['Y', 'y']):
				print 'You answered "No", so skip this SDK refname.'
				return False # False: cache->localdir sync should be skipped.
		
	for fp_src, fp_dst in cache_to_local_enum_pair(section, dsection, dir_refname_old, localdir):
#		print ">>> fp_src=%s"%(fp_src); print "### fp_dst=%s"%(fp_dst); print #debug
		if not os.path.exists(fp_dst):
			continue
		elif os.path.isfile(fp_dst):
			os_remove_easy(fp_dst)
		elif os.path.isdir(fp_dst):
			rmdir_if_empty(fp_dst)
		else:
			print "!!!Error on %s"%(fp_dst)
			assert 0
		# Note: actual cache->localdir copy will be done later in sync_sdkcache_to_sdklocal()
	
	if is_remove_old:
		force_rmtree(dir_refname_old)
	
	return True # True: cache->localdir sync should be carried out.


def sdk_refname_match_list(refnames, patterns):
	refname_matches = []
	for refname in refnames:
		for pattern in patterns:
			if ('*' in pattern) or ('?' in pattern):
				if fnmatch.fnmatch(refname, pattern):
					refname_matches.append(refname)
					break
			else:
				if refname.find(pattern)>=0:
					refname_matches.append(refname)
					break
	return refname_matches


class Action:
	def __init__(self):
		self.upcache = True # whether update $/sdkbin-cache/<sdk_refname>
		self.uplocal = True # whether update $/sdkin for current <sdk_refname>

def pick_sdk_refnames(iniobj, ini_dir):
	# Check all refname's status, check for errors and print the summary.
	# Return user-picked refnames via daction dict.
	daction = {} # dict of Action, daction[sdk_refname]=Action()
		
	# check required INI key:
	for section, dsection, sdk_refname, localdir in enume_sections(iniobj, ini_dir):
		for ik_required in [IK_svndatetime, IK_svnurl, IK_localdir]:
			if not ik_required in dsection:
				raise('Scalacon Error: INI section [%s] missing %s= .'%(section, ik_required))
	
	picked_refnames = []
		# If empty, it means user cares for all refnames.
		# If non-empty, it means user only cares for those refnames.
	
	is_interactive = not g_isforce
	is_all_ready = True # assume init True
	
	while True:
		daction = {}
		all_refnames = []
		# print summary:
		print "The following SDK repos are being requested:"
		idx = 0
		for section, dsection, sdk_refname, localdir in enume_sections(iniobj, ini_dir):

			if g_sdkbin_limits and (not sdk_refname_match_list([sdk_refname], g_sdkbin_limits)):
				continue

			all_refnames.append(sdk_refname)

			if is_interactive:
				if picked_refnames and (not sdk_refname in picked_refnames):
					continue # skip this refname
			
			action = Action()
			daction[sdk_refname] = action

			idx += 1
			idxshow = "(%d)"%(idx)
			print '%-4s'%(idxshow)
			print '    [%s] refname="%s"'%(section, sdk_refname)
			print "    svndatetime: %s"%(dsection[IK_svndatetime])
			print "    svnurl     : %s"%(dsection[IK_svnurl])
			print "    localdir   : %s"%( os.path.join(ini_dir, dsection[IK_localdir]))
			
			cached_svndt = check_cached_svndatetime_1refname(dsection, sdk_refname)
			if cached_svndt==dsection[IK_svndatetime]:
				action.upcache = False
				str_cache_status = 'match'
				cache_state_asterisk = ' '
			elif cached_svndt=='not_exist':
				action.upcache = True
				str_cache_status = 'not exist'
				cache_state_asterisk = '*'
			else:
				action.upcache = True
				str_cache_status = 'not match(was %s)'%(cached_svndt)
				cache_state_asterisk = '*'
			
			mlocal_sigfile = get_mlocal_sigfile_1refname(localdir, sdk_refname)

			uplocal_reason = [] # may contain multiple reasons
			if action.upcache==True:
				action.uplocal = True
				uplocal_reason.append('cache will update')
			else:
				if not os.path.exists(mlocal_sigfile):
					action.uplocal = True
					uplocal_reason.append("missing localdir signature '%s'"%(os.path.basename(mlocal_sigfile)))
				elif is_A_older_than_B(mlocal_sigfile, g_ini_filepath): # special: A(mlocal_sigfile) is consider older if not exist
					action.uplocal = True
					uplocal_reason.append('%s changed'%(os.path.basename(g_ini_filepath)))
				else:
					action.uplocal = False
			
			print '  %s Cache status: %s'%(
				cache_state_asterisk, 
				str_cache_status,
				)
			print  '  %s Localdir need update: %s %s'%(
				'*' if action.uplocal else ' ',
				'yes' if action.uplocal else 'no', 
				'(reason: %s)'%(';'.join(uplocal_reason)) if uplocal_reason else ''
				)

			try: 
				print '    Comment: %s'%(dsection[IK_comment])
			except KeyError:
				pass

			if action.uplocal:
				is_all_ready = False
		
		print
		
		if all_refnames==[]: # user command line passed in bad limit-patterns
			raise GetsdkError('No matching SDK refnames found. You probably gave wrong --sdkbin-limit=<patterns> .')

		if is_interactive and not is_all_ready:
			def get_answer():
				while True:
					a = raw_input('The above SDKs will be updated. Is it OK? [Yes/No/Reset/(filter)] ')
					if a in ['Y','y']:
						return 'y'
					elif a in ['N','n']:
						return 'n'
					elif a in ['R','r']:
						return 'r'
					elif len(a)>1:
						pattern = a
						picked_olds = picked_refnames if picked_refnames else all_refnames
						picked_news = sdk_refname_match_list(picked_olds, [pattern])
						if picked_news:
							print
							print 'OK. SDK repo refname filtered.'
							print
							return picked_news
						else:
							print
							print "The filter word('%s') matches nothing. Try again."%(pattern)
							print
					else:
						print 'Invalid input. Valid are single letter y,n,r or more than one letter as filter word.'
						print 'Examples:'
						print '   vc100'
						print '  *x64'
						print '   *dev*'
			a = get_answer()
			if type(a)==type(''):
				if a=='y':
					return daction
				elif a=='n':
					print 'You answered No. Now quit.'
					exit(2)
				elif a=='r':
					print
					print 'OK. SDK repo refname reset.'
					print
					picked_refnames = []
			else:
				picked_refnames = a
		
		else: # non-interactive
			return daction



def store_vcX0_version_hint(localdir):
	content = """cidver and Visual C++ version relation:
vc60  = Visual C++ 6.0 (1998)
vc71  = Visual C++.NET 2003
vc80  = Visual C++ 2005
vc90  = Visual C++ 2008
vc100 = Visual C++ 2010
vc110 = Visual C++ 2012
vc120 = Visual C++ 2013
vc140 = Visual C++ 2015
"""
	dir_cidvers = os.path.join(localdir, 'cidvers')
	if not os.path.isdir(dir_cidvers):
		return # ignore this
	
	hint_filepath = os.path.join(dir_cidvers, 'vcX0.version-hint.txt')
	if os.path.exists(hint_filepath):
		return
		
	existing_cidvers = os.listdir(dir_cidvers)
	for cidver in existing_cidvers:
		if cidver.startswith('vc'):
			open(hint_filepath, 'w').write(content)
			return


def do_getsdks():
	iniobj = ConfigParser.ConfigParser()
	global g_cidvers_restrict
	
	try:
		readret = iniobj.read(g_ini_filepath)
		
		# Override the values in [DEFAULT] section according to env-vars
		kvpairs = iniobj.items('DEFAULT')
		dpairs = dict(kvpairs)
		for key,value in kvpairs:
			# Check all upper-case then lower-case keys against env.
			# Code here does not cope with mixed-case env-var names for simplicity, 
			# so user should obey this when setting env-var.
			if key.upper() in os.environ:
				value = os.environ[key.upper()]
			elif key.lower() in os.environ:
				value = os.environ[key.lower()]
			else:
				continue
			iniobj.set('DEFAULT', key, value) # dpairs[key] = value
		
		if ('cidvers_restrict' in dpairs) and (dpairs['cidvers_restrict']!='0'):
			g_cidvers_restrict = dpairs['cidvers_restrict'].split()
		
	except(MissingSectionHeaderError):
		print 'Scalacon Error: "%s" does not look like a valid INI file.'%(g_ini_filepath)
		exit(1)

	if not readret:
		print 'Scalacon Error: The INI file "%s" does not exist or cannot be opened.'%(g_ini_filepath)
		exit(1)
	
	daction = pick_sdk_refnames(iniobj, g_ini_dir) # may do interactive work inside
		# For any picked refname, daction[refname] is an Action object.
	assert daction
	
	for section, dsection, sdk_refname, localdir in enume_sections(iniobj, g_ini_dir):
		dir_sdkcache, dircache_this_refname = cachedirs(sdk_refname)[:2]
	
		if g_sdkbin_limits and (not sdk_refname_match_list([sdk_refname], g_sdkbin_limits)):
			continue
		
		if not sdk_refname in daction:
			continue
	
		action = daction[sdk_refname] # info collected by pick_sdk_refnames
	
		if action.upcache:
			print '[%s]Creating cache in "%s" ...'%(section, dircache_this_refname)
			fetch_sdkcache_1refname(section, dsection, sdk_refname, localdir) #!!!
		
		# verify the cache is refreshed, otherwise assert fail.
		try:
			cached_svndatetime = open(os.path.join(dircache_this_refname, FN_SVNDATETIME_CKT), 'rb').read()
		except IOError:
			cached_svndatetime = 'none' # arbitrary string
		assert dsection[IK_svndatetime] == cached_svndatetime

		go_on_sync = True
			# It will be false if user cancels it inside clean_old_local_by_old_refname().
		
		# Now we are going to clean up the old files in $/sdkin according to refname.old's content
		if action.upcache:
			# This copes with new content grabbed from svn server.
			assert action.uplocal==True
			go_on_sync = clean_old_local_by_old_refname(section, dsection, 
				os.path.join(g_ini_dir, DIRNAME_CACHE, sdk_refname+SUFFIX_OLD), # diff1 (+SUFFIX_OLD)
				localdir, True) #!!! diff2
		elif action.uplocal:
			# This copes with get-sdkin.ini change that would cause cidver-mapping change.
			go_on_sync = clean_old_local_by_old_refname(section, dsection, 
				os.path.join(g_ini_dir, DIRNAME_CACHE, sdk_refname), # diff1
				localdir, False) #!!! diff2

		if not go_on_sync:
			print
			continue
				# This leave FN_PATTERN_REFNAME_DONE sigfile not updated, so run this py again
				# will cause this refname's cache->localdir sync to launch again, so you user will 
				# again be asked whether to overwrite/remove those files. This is desired behavior.

		# Determine whether to sync cache to $/sdkin (mlocal)
		if action.uplocal:
			print '[%s]Syncing cache to localdir ...'%(section)
			sync_sdkcache_to_sdklocal(section, dsection, sdk_refname, localdir) #!!!
			print '[%s]Stored in localdir: %s'%(section, localdir)
			print
	
			# Make the exported "include"(.h) files read-only. 
			# (TO IMPROVE: If more than one sdkin share the same localdir, there will be duplicate make-read-only actions.)
			for root, dirs, files in os.walk( os.path.join(localdir, "include") ):
				for file in files:
#					print 'Make read-only:', root+os.sep+file #debug
					os.chmod(root+ '/' +file, stat.S_IREAD)
	
	if os.name=='nt':
		store_vcX0_version_hint(localdir)
	elif os.name=='posix': # Linux or MAC
		create_linuxgcc_symlink(localdir)
	
	return 0

def create_linuxgcc_symlink(localdir):
	# When running on Linux, we create a symlink called $/sdkin/cidvers/linuxgcc pointing to
	#	$/sdkin/cidvers/gcc4.8_i686
	# or
	#	$/sdkin/cidvers/gcc4.8_x64
	# according to 
	# * whether current system is 32-bit or 64-bit
	# * The 4.8 is the smallest version number we found. That is if gcc_4.8_x64 and gcc_6.3_x64
	#   are both found, we'll use gcc_4.8_x64 .
	cidver_ptn = 'gcc*_x64' if ('x86_64' in os.uname()) else 'gcc*_i686'
	dir_cidvers = os.path.join(localdir, 'cidvers')
	subdirs = os.listdir(dir_cidvers)
	gcc_subdirs = fnmatch.filter(subdirs, cidver_ptn)
	if not gcc_subdirs:
		print "Info: In '%s', no subdir matches pattern '%s', so skip linuxgcc symlink creation."%(dir_cidvers, cidver_ptn)
		return
	
	def cmp_verstr(v1, v2):
		# Compare version string: https://stackoverflow.com/a/11887885
		# For example: 4.12 > 4.8 > 4.1.2
		# So we cannot simply compare by float() them.
		if StrictVersion(v1)==StrictVersion(v2):
			return 0
		elif StrictVersion(v1)<StrictVersion(v2):
			return -1
		else:
			return 1
	
	gcc_dirs_sorted = sorted(gcc_subdirs, cmp_verstr, lambda x:re.sub(r'gcc([0-9.]+)_x64', r'\1', x))
	symlink_target = gcc_dirs_sorted[0]
	
	symlink_source = os.path.join(dir_cidvers,'linuxgcc')
	
	if os.path.islink(symlink_source):
		os.remove(symlink_source)
	
	if not os.path.exists(symlink_source):
		print 'Creating symlink in localdir: linuxgcc -> %s'%(symlink_target)
		os.symlink( symlink_target, symlink_source ) # memo: no need to add dir-prefix for symlink_target


def main():
	global optdict, g_ini_filepath, g_ini_dir, g_isforce
	global g_is_do_self, g_is_only_self, g_self_dir_param
	global g_is_svn_checkout, g_sdkbin_limits
	global g_is_simulate

	optlist,arglist = getopt.getopt(sys.argv[1:], '', 
		['force', 'ini=', 'self=', 'get-all', 'simulate', 
		'use-svn-checkout', 'sdkbin-limit=',
		'version'])
	optdict = dict(optlist)
	
	if '--version' in optdict:
		print '%s v%s'%(os.path.basename(__file__), version)
		return 0;

	if '--ini' in optdict:
		g_ini_filepath = os.path.normpath( os.path.abspath(optdict['--ini']) )
			# convert to backslashes is required for later code!
		g_ini_dir = os.path.split(g_ini_filepath)[0]
	else:
		sys.stderr.write('Error: You need to assign an INI file describing the SDKs to get(--ini=xxx.ini).\n')
		return 1
		
	if '--sdkbin-limit' in optdict:
		g_sdkbin_limits = optdict['--sdkbin-limit'].split(',')
		
	if '--force' in optdict:
		g_isforce = True
		
	if '--use-svn-checkout' in optdict:
		g_is_svn_checkout = True

	if '--self' in optdict:
		g_is_do_self = True
		g_is_only_self = True
		g_self_dir_param = optdict['--self']
		
	if '--get-all' in optdict:
		g_is_do_self = True
		g_is_only_self = False

	if '--simulate' in optdict:
		g_is_simulate = True

	ret = do_getsdks()
	
	if ret==0:
		print "[Success]"
	
	return ret
	

if __name__ == '__main__':
	thispy = os.path.basename(__file__)
	errprefix = '%s error: '%(thispy)
	try:
		ret = main()
	except GetsdkError as e:
		sys.stderr.write(errprefix + e.errmsg + '\n')
		exit(1)
	
	exit(ret)
