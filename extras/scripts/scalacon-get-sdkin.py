#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取一个或多个外来的 SDK 二进制文件到本地，成为本地 SDK 。

--ini=<ini-filepath>
	[必须] 描述外来 SDK 的 ini 文件。

--force
	[可选]
	强制模式。意思是，对于每一条外来 SDK 描述，先将其指示的本地目录清空。
	所有本地目录条目都清空后，再从各条 SDK 的 svnurl 抓取内容，以此保证
	本地目录中不存在已废弃的文件。
	.
	如果不用 --force, 则不作任何清空动作，且，处理每一个 SDK 条目时，若
	本地目录已经存在（不管里面的内容如何）就跳过服务端抓取动作。

--self=[<dir-sdkout>]
	[可选]
	仅取 [self] 小节的内容。不指定则只会取其他小节(sdkin)的内容。
	本选项的值指出将 self 内容取到哪个本地目录中（覆盖 gmb_dirname_sdkout）。
	如果 = 后是空值，则 localdir 仍旧遵照 INI 中的描述。

--get-all
	[可选]
	取 sdkin 和 sdkout 。即使用了 --self ， --get-all 也生效。

--simulate or -s
	[可选]
	模拟运行，不进行实际的本地文件操作，仅显示需要进行的动作。

=== >>> INI 格式范例

[DEFAULT]
NLSSVN=https://nlssvn/svnreps
gmb_dirname_sdkin=sdkin
gmb_dirname_sdkout=sdkout

[sdkin.common-include]
svndatetime= 2016-03-05 23:00
svnurl=      %(NLSSVN)s/CommonLib/common-include/trunk
localdir=    %(gmb_dirname_sdkin)s/include
want-cidver-mapping=1
; -- localdir is relative to this INI file.
implicit-cidver-mapping=
explicit-cidver-mapping=

[sdkin.mm_snprintf]
svndatetime= 2016-03-06 13:39:43
svnurl=      %(NLSSVN)s/scalacon/sdkbin/mmsnprintf/4.2.0
localdir=    %(gmb_dirname_sdkin)s
want-cidver-mapping=1

[self.0]
svndatetime= 2016-03-11 11:44:00
svnurl=      %(NLSSVN)s/scalacon/sdkbin/IUartBasic/2.1.6
localdir=    %(gmb_dirname_sdkout)s
want-cidver-mapping=1


=== <<< INI 格式范例

[DEFAULT] 小节用来定义一些全局变量的默认值，以便稍后多次引用。

[DEFAULT] 中定义的条目会被同名环境变量覆盖，这个覆盖动作是在本 .py 代码中实现的。

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

version = "1.2"
optdict = {}
g_ini_filepath = '' # the config file(in INI format)
g_ini_dir = ''
g_isforce = False
g_is_do_self = False
g_is_only_self = False
g_self_dir_param = ''

g_is_simulate = False

DIRNAME_CACHE = 'sdkin-cache'

g_required_subdir_in_sdkin = ['include', 'cidvers' ]

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


def force_rmtree(dir):
	# Remove read-only attribute for files inside.
	for root, dirs, files in os.walk(dir):
		for file in files:
			os.chmod(root+'/'+file, stat.S_IWRITE)

	# Then remove the whole tree.
	if os.path.isdir(dir):
		shutil.rmtree(dir)
	
def copytree_overwrite(src, dest, ignore=None):
	# Thanks to: http://stackoverflow.com/a/15824216/151453
	if os.path.isdir(src):
		if not os.path.isdir(dest):
			os.makedirs(dest)
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
		shutil.copyfile(src, dest)


def pick_sections(iniobj, g_ini_dir):
	sdknames = iniobj.sections()
	for section in sdknames:
		if section.startswith('self.') and not g_is_do_self:
			continue
		if (not section.startswith('self.')) and g_is_only_self:
			continue
		
		if not section.startswith('sdkin.'):
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
		yield section, dsection, localdir_final # dsection's d implies dict


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

def getsdk_with_cidver_mapping(section, svnurl, svndatetime, localdir, 
	implicit_mapping_spec, explicit_mapping_spec):
	# section is section name,
	# all other params are items from this section.
	# im/explicit_mapping_spec sample: "vc100(=vc80) vc100x64(=vc80x64)"
	# [PENDING] g_isforce processing ........
	
	sdk_refname = re.sub(r'^sdkin\.', '', section)
	cachedir = os.path.join(g_ini_dir, DIRNAME_CACHE, sdk_refname)
	svncmd = 'svn export --force "%s@{%s}" "%s"'%(svnurl, svndatetime, cachedir)
	print "Running cmd: \n  " + svncmd
	
	if g_is_simulate:
		return 
	
	ret = subprocess.check_call(shlex.split(svncmd))
	
	### Apply four-layer cid-mapping

	cidvers_dir = os.path.join(cachedir, 'cidvers')
		# cidvers_dir is expected to contain sub-dirs like vc60, vc80, vc100x64 etc
	mapping = {} # mapping[virtual]=real
		# Example: 
		#	mapping['vc100']=['vc90', 'vc80']
		# means:
		# SDK-user's vc100 will be mapped to vc90; some previous layer has mapped it to 'vc80' but has been overridden.
		# I record the overridden info just for debugging purpose.
	
	# layer 1: real <cidver> folder, vc60, vc80 etc 
	list_cidvers = os.listdir(cidvers_dir)
	assert list_cidvers
	for cidver in list_cidvers:
		mapping[cidver] = [cidver]
	
	# layer 2: cidver-mapping.ini
	self_mapping_ini = os.path.join(cachedir,'cidver-mapping.ini')
	if os.path.isfile(self_mapping_ini):
		merge_sdk_self_mapping(mapping, self_mapping_ini)
	
	# layer 3: SDK-user implicit mapping
	if implicit_mapping_spec:
		implicit_mapping_dict = make_cidver_mapping_dict(implicit_mapping_spec)
		for virtual_cidver in implicit_mapping_dict.keys():
			if not virtual_cidver in mapping:
				# add this mapping only in case of not exist
				mapping[virtual_cidver] = implicit_mapping_dict[virtual_cidver]
	
	# layer 4: SDK-user explicit mapping
	if explicit_mapping_spec:
		explicit_mapping_dict = make_cidver_mapping_dict(explicit_mapping_spec)
		for virtual_cidver in explicit_mapping_dict.keys():
			# use this mapping
			mapping.setdefault(virtual_cidver, [])
			mapping[virtual_cidver].insert(0, explicit_mapping_dict[virtual_cidver])
	
	for subdir in g_required_subdir_in_sdkin:
		copytree_overwrite(
			os.path.join(cachedir, subdir),
			os.path.join(localdir, subdir))

	# Now, generate virtual cidver dirs(directly in localdir) by copying from their real bodies
	for virtual_cidver in mapping:
		real_cidver = mapping[virtual_cidver][0]
		dir_src = os.path.join(cachedir, 'cidvers', real_cidver)
		dir_dst = os.path.join(localdir, 'cidvers', virtual_cidver)
		
		if not os.path.isdir(dir_src):
			# try link layer(3-4) to layer 2 (just a recursive mapping operation)
			real_cidver = mapping[real_cidver][0]
			dir_src = os.path.join(cachedir, 'cidvers', real_cidver)
			if not os.path.isdir(dir_src):
				print 'Scalacon Error: You request mapping "%s" to real cidver "%s" but the directory "%s" does not exist, '\
					'which means that input SDK(INI section [%s]) does not provide that cidver.'%(
					virtual_cidver, real_cidver, dir_src, section)
				exit(25)
		
		copytree_overwrite(dir_src, dir_dst)
		
		# create an empty file telling user the cidver's real body
		if virtual_cidver != real_cidver:
			filename_cidver_source_hint = "_[%s]CopiedFromCidver.%s.txt"%(section, real_cidver)
			open(dir_dst+'/'+filename_cidver_source_hint, "wb").close()


def getsdk_direct(section, svnurl, svndatetime, localdir):
	if (not g_isforce) and os.path.exists(localdir):
		print 'Existed localdir "%s", skipped.'%(localdir)
		return
	
	svncmd = 'svn export --force "%s@{%s}" "%s"'%(svnurl, svndatetime, localdir)
	print "Running cmd: \n  " + svncmd
	
	if g_is_simulate:
		return
	
	ret = subprocess.check_call(shlex.split(svncmd))


def do_getsdks():
	iniobj = ConfigParser.ConfigParser()
	
	try:
		readret = iniobj.read(g_ini_filepath)
		
		# Override the values in [DEFAULT] section according to env-vars
		kvpairs = iniobj.items('DEFAULT')
		for key,value in kvpairs:
			# Check all upper-case then lower-case key in env, for OS like Linux.
			if key.upper() in os.environ:
				value = os.environ[key.upper()]
			elif key.lower() in os.environ:
				value = os.environ[key.lower()]
			else:
				continue
			iniobj.set('DEFAULT', key, value)
		
	except(MissingSectionHeaderError):
		print 'Scalacon Error: "%s" does not look like a valid INI file.'%(g_ini_filepath)
		return 1

	if not readret:
		print 'Scalacon Error: The INI file "%s" does not exist or cannot be opened.'%(g_ini_filepath)
		return 1
	
	if g_isforce:
		# 删除目录动作要专门自己一个循环（而非在 fetch server content 循环中），
		# 是考虑到各个 SDK 指定的 localdir 可能有重叠或父子关系，那将导致后一次循环的
		# rmtree 将前一次循环取出的东西给删了。
		for s,ds, localdir_final in pick_sections(iniobj, g_ini_dir):
			print 'Removing old directory: %s'%(localdir_final)
			if g_is_simulate:
				continue
			force_rmtree(localdir_final)
		
		# 删除 cidver cache 目录
		force_rmtree( os.path.join(g_ini_dir, DIRNAME_CACHE) )

	# For each SDK, fetch server content.
	for section, dsection, localdir in pick_sections(iniobj, g_ini_dir):

		svnurl = dsection['svnurl']
		svndatetime = dsection['svndatetime']
		
		try:
			want_cidver_mapping = dsection['want-cidver-mapping']
			implicit_mapping_spec = dsection.setdefault('implicit-cidver-mapping', '')
			explicit_mapping_spec = dsection.setdefault('explicit-cidver-mapping', '')
		except:
			want_cidver_mapping = False
		
		print "SDK[%s] from %s"%(section, svnurl)

		if want_cidver_mapping:
			getsdk_with_cidver_mapping(section, svnurl, svndatetime, localdir, implicit_mapping_spec, explicit_mapping_spec)
		else:
			getsdk_direct(section, svnurl, svndatetime, localdir)
		
		# Make the exported files read-only. 
		# (TO IMPROVE: If more than one sdkin share the same localdir, there will be duplicate make-read-only actions.)
		for root, dirs, files in os.walk(localdir):
			for file in files:
#				print 'Make read-only:', root+os.sep+file #debug
				os.chmod(root+ '/' +file, stat.S_IREAD)
		
	return 0

def main():
	global optdict, g_ini_filepath, g_ini_dir, g_isforce
	global g_is_do_self, g_is_only_self, g_self_dir_param
	global g_is_simulate

	optlist,arglist = getopt.getopt(sys.argv[1:], 's', 
		['force', 'ini=', 'self=', 'get-all', 'simulate', 'version']
		)
	optdict = dict(optlist)
	
	if '--version' in optdict:
		print '%s v%s'%(os.path.basename(__file__), version)
		return 0;

	if '--ini' in optdict:
		g_ini_filepath = optdict['--ini']
		g_ini_dir = os.path.split(g_ini_filepath)[0]
	else:
		sys.stderr.write('Error: You need to assign an INI file describing the SDKs to get(--ini=xxx.ini).\n')
		return 1
		
	if '--force' in optdict:
		g_isforce = True

	if '--self' in optdict:
		g_is_do_self = True
		g_is_only_self = True
		g_self_dir_param = optdict['--self']
		
	if '--get-all' in optdict:
		g_is_do_self = True
		g_is_only_self = False

	if ('--simulate' in optdict) or ('-s' in optdict):
		g_is_simulate = True

	ret = do_getsdks()
	return ret
	

if __name__ == '__main__':
    ret = main()
    exit(ret)
