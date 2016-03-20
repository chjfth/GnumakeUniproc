#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
扫描符合 Scalacon 规范的函数库的 SDK 输出目录，搜寻所有的 pdb 文件，获知 pdb 关联的源码文件，
对于这些源码文件进行“source indexing”动作，即，给源码文件对应 svn checkout 命令，将这些
命令组织好后嵌回 pdb，以达到用 Visual C++ 2005（或更新版本）调试程序时能自动准确地 checkout
源码的目的。

该程序用于替代微软官方 Debugging Tools for Windows 中附带的 ssindex.cmd＋svn.pm。我发现
微软提供的那个默认 source indexing 方案有诸多缺陷！

注：
* 目前此程序仅针对 Visual C++ 的输出有效（x86,x64,WinCE），因为其处理的是 pdb 文件。

名词：

sew: 缝合的意思。我用该词来替代“source indexing”，因为 indexing 已经在软件界用得太泛滥。
	“Sew a source file”指的是找到一个源文件所对应的 svn checkout 命令，并将此对应关系形成
		SRCSRV: source files ---------------------------------------
	小节中的一句话。
	“Sew a pdb”指的是将一个 srcsrv 流嵌入 pdb 的动作。

cookie: 即是指被缝合的一个源文件。

track: 一个轨道。一个轨道是 pdb 中、SRCSRV 流中、SRCSRV 小结下的一行信息。这样的一行信息
	描述了一个源文件的各个 varX 属性。 （例子在程序完成后补充）


输入参数：

--dir-pdb=<dp>
	[必须]
	指出在哪个目录中搜索 pdb 。

--dir-source=<ds>
	[必须]
	指出仅考虑对那个目录中的源文件作 sew 动作。
	背景：用 srctool -r xxx.pdb，会列出很多源文件，其中很多是微软构建机上的源文件，比如
		f:\sp\vctools\crt_bld\self_x86\crt\src\wchtodig.c
		f:\sp\vctools\crt_bld\self_x86\crt\src\atox.c
	我们不需对那些微软的 .c 作 sew 动作。我们很容易区分那些源文件和我们自己的源文件，
	因为我们自己的源文件会放在(比如) P:\nlsbuild 目录下，而非 f:\sp 下。

--datetime-co=<dtco>
	[必须]
	告知一个时间戳，格式如 "2011-08-29 08:30:00" ，指出用户要缝合的 svn checkout 命令应该
	用哪个时间戳。是的，在我的设计中，不是用 SVN 版本号来标识一个具体的版本，而是用时间戳。
	scalacon-ssindex-svn.py 自身无法得知这个时间戳，构建源码的人才知道，因此要由外部传入。
	.
	<dtco> 填为 now ，则自动取当前时间。
	.
	我不让此参数可选，因为时间太重要了，它决定你是否将 checkout/export 正确的版本。

--dir-reposie-table=<drt>
	[必须] 但指定了 --loosy-reposie-table 的情况下可选。
	这个参数跟陈军给 NLSCAN SVN server 设计的目录结构有极大关系。
	指出一个本地目录，将在此目录下寻找一个 reposie-<svnhostid>.txt 文件。

	<svnhostid> 的实地取值是由源文件的 SVN URL 加上 <svnhosttable> 推导出来的。
	举例：对于我们公司， <svnhostid> 的最常见取值是 nlssvn。

	reposie-nlssvn.txt 文件格式如下：

	Isyslib/IUartBasic	gpbr_071126_IUartBasic
	CommonLib/gadgetlib	gpbr_080812_gadgetlib
	...

	每行是一个表项，每个表项两列，第一列我给它命名为 reposie，在 SVN 服务器的根路径
	（https://nlssvn/svnreps）之下，拼上 reposie ，就得到一个“SVN 工程”的根路径。
	一个 SVN URL 是否是“工程根路径”，其判断特征是此路径下是否有 trunk, branches 子目录。
	比如，例子中的第一项，拼上 reposie 后得到：

		https://nlssvn/svnreps/Isyslib/IUartBasic

	表项的第二列称为 gpbr code ，用 gpbr code 作为环境变量名称查值，查到的值称作 branchie，
	branchie 指出对于当前的 SVN 工程根使用哪个分支。比如，环境变量中有

		gpbr_071126_IUartBasic=branches/4.2

	则，*匹配的*源文件对于的 SVN checkout 地址即是

		https://nlssvn/svnreps/Isyslib/IUartBasic/branches/4.2

	另：
	* 若 gpbr_071126_IUartBasic 环境变量不存在，则默认为 --default-branchie 指定的分支 。
	* 若 gpbr_071126_IUartBasic 环境变量存在、但和 匹配的本地源文件通过 svn info 查到的不符，
	  则宣告发生错误。

--default-branchie=<dftbr>
	[可选]
	默认为 trunk 。

--loosy-reposie-table
	[可选] （简称 LRT or lrt）
	这个一般供开发人员做实验用。
	使用此参数，则允许不提供 --dir-reposie-table，
	* 就算提供了 --dir-reposie-table，也允许相应的 reposie-table 文件（如 reposie-nlssvn.txt）不存在，
	* 就算 reposie-table 文件存在，也允许找不到匹配的 reposie，
	* 找不到匹配的 reposie 的情况下，在 urm 中搜索 "/<dftbr>"，搜索到则可拆解出 branchie 和 reposie 。

--svn-use-export
	[可选]
    若启用此开关，则在 srcsrv 流中嵌入 svn export 命令而非 svn co 。

--svnhost-table=<svnhosttable>
	[必须]
	此值是一个本地文件名（可带路径）或一个文件的 SVN 地址。
	该值指示的文件是一个表格，每行有两个字段，用于将源码 SVN URL 的前缀关联到一个“主机名”。
	比如：svnhosttable 内容如下：

		nlssvn	https://nlssvn/svnreps
		chjsvn	http://chjsvn.dev.nls

	作用是，当我们用 svn info 查出一个源码文件的 URL 为 https://nlssvn/svnreps/Isyslib/IUartBasic/dev/libsrc/mswin/UartBasic_win.cpp ，
	则查找 svnhosttable 可知此 URL 对应的 svn 主机名为 'nlssvn'，该“主机名”的意义在于：
	<drt> 配合上该主机名才能查出此 svn 主机对应的 reposie-table（此环节的查法见 --dir-reposie-table 的解释）。
	.
	此值若是 SVN URL，则将那个文件 svn cat 到当前目录。
	.
    用的地方： MatchSvnHostId() & GetSvnRootUrl()

--pick-cherries=<cherry1>,<cherry2>,...
--pick-sstreams-dirs=<pickdir1>,<pickdir2>,...
	[可选] since v1.2.
	这两个参数指定将额外的文件内容追加入 PDB 的 S 流，此两参数需一起使用。 比如：
	
	--pick-cherries=mm_snprintf,ithreadsync
	--pick-sstreams-dirs=D:\mydir1,D:\mydir2
	
	表示：
		在给 'srctool -r self.pdb' 缝合 S 流时，额外去 D:\mydir1 , D:\mydir2 中搜索
	mmsnprintf.sstream.txt, ithreadsync.sstream.txt ，如果它们存在，将它们的内容加入
	self.pdb 的 S 流（当然，只取 "SRCSRV: source files" 小节的内容）。
	
	pickdir 的特殊形式： 如果 pickdir 以 ! 打头，表示本目录是相对于当前 pdb 的。比如，
	指定了 --pick-sstreams-dirs=!.. ，那么，处理 D:/sdkin/vc100/bin-debug/foo.pdb 时，
	会到 D:/sdkin/vc100 中寻找 <cherry>.sstream.txt 。
	
	--pick-cherries 的特殊形式： 如果 --pick-cherries=* ，那么所有 pickdir 中的 
	所有 .sstream.txt 都会被加入。多个 pickdir 若中有同名的文件，它们的内容都将加入。

	层级关系： --pick-cherries 作为外层循环， --pick-sstreams-dir 作为内层循环；
	在某个搜索目录中遇到匹配的 <cherry>.sstream.txt 之后，仍会继续搜索其他目录并将所有 S 流加入。
	
	此设施是为了解决这样一个问题：对于将静态库(.lib) 提供给用户作 SDK 的情况，静态库中的代码
	按普通方法是做不了 pdb sewing 的。我的意思是，如果你提供 foo.lib 以及配套的 foo.lib.pdb
	给用户使用，用户将其链接到自己的 bar.exe 里头（同时得 bar.pdb）；虽然 foo 的代码都融合
	到了 bar.exe 中，但是用户手上并没有 foo 的源代码，用户仅能通过 srctool -r bar.pdb 查得
	foo 相关源码的原始本地路径，至于这些本地路径如何转换成远程抓取命令则一无所知。
	
	这时候可以怪一怪微软为什么不让 .lib.pdb 是可以 sewing 的，且 sewing 内容能够融合到 exe.pdb 中。
	（ srctool -r xxx.lib.pdb 将返回空 ）
	
	我对此有一个解决方法：拿 mm_snprintf 为例，虽然 mm_snprintf.lib.pdb 无法被 sewing ，
	但 mm_snprintf.dll 是可以的，我为其生成 mm_snprintf.pdb 时当场将其 S 流
	明明白白存一份成 mmsnprintf.sstream.txt ，我们可以相信，假想微软允许 mm_snprintf.lib.pdb 
	被 sewing ，那么其 S 流的内容肯定跟 DLL pdb 的 S 流一模一样。这就好了，假定 bar.exe 
	静态链接了 mm_snprintf.lib ，那么，我们对 bar.exe 进行 sewing 时，就可以把对应的 DLL pdb 
	S 流内容（仅 SRCSRV: source files 小节）追加到 bar.pdb 中，sewing 目的就达成了。
	
	另，变量命名出现的 cherry-pick 指的就是这个。

--save-sstreams-dir=<ssdir>
	[可选] since v1.2.
	保存一个 sstream 文件。假定 pdb 的文件名是 foo.lib.pdb 或 foo.pdb ,
	则生成的文件名是 foo.sstream.txt ，生成的目标目录由 <ssdir> 告知。 
	<ssdir> 可以是绝对目录或相对目录（相对于进程当前工作目录）。但，如果 <ssdir> 以 ! 打头，
	则指明一个相对于 pdb 文件的目录。
	比如，当前正在处理 D:/sdkin/vc100/bin-debug/foo.pdb ， 传入 ssdir=!.. ，
	那么将得到 D:/sdkin/vc100/foo.sstream.txt 。
	.
	保存出的 sstream 文件，可以由 --pick-sstreams 使用，用途详见 --pick-sstreams 的说明。
	.
	Memo: 同一个 <ssdir> 中可能会存储多个 .sstream.txt 文件，因此本参数名中 sstreams 是复数形式。
	而单个 .sstream.txt 中只会存放一个 S 流，因此文件名中的 stream 是单数形式。
	.
	如果当前处理的 pdb 有 cherry-picking 行为，那么，针对此 pdb 的 save-sstream 动作生成的
	.sstream.txt 将包含 cherry-picking 的内容。

--pick-sstreams-dirs-from-ini=<inipath>
--pick-sstreams-dir-sdkin=<dirsdkin>
	[可选] since v1.2.
	类似于 --pick-sstreams-dirs (但优先于它)，指定从 inipath 中搜索出 pickdirs 。 

--src-mapping-pdb=<dirpfxpdb>
--src-mapping-svn=<dirpfxsvn>
	[可选] since v1.2.
	本程序处理 srctool -r xxx.pdb 列出的每一个 cookie 时，会先进行 dirpfxpdb -> dirpfxsvn 
	目录前缀映射（如果 cookie 符合 dirpfxpdb 前缀），对于映射后的路径执行 svn info 
	（而非对原始 cookie 路径执行）。
	
	此两选项用于解决这样一个问题：
		假设你的 svn 沙箱路径为 d:\mywork , 里头的子目录 d:\mywork\examples 用于存放例子代码，
	你试图编译例子时是将 d:\mywork\examples 拷贝到 d:\verify\examples 去编译，结果，你对
	编译得到的 EXE 进行 PDB-sewing 时，d:\verify\examples\foobar.c 并不会被 sewing ，原因是 
	``svn info d:\verify\examples\foobar.c`` 不会返回一个 SVN URL 。没有这个 SVN URL 信息，
	本程序是无法知道如何对 d:\verify\examples\foobar.c 进行 sewing 的。
	解决方法是，在 CalTrack(cookie) 中，将 cookie 由 d:\verify\examples\foobar.c 替换为
	d:\mywork\examples\foobar.c ，``svn info d:\work\examples\foobar.c`` 是可以返回 SVN URL 的。
	有了 SVN URL, 此 cookie 的 sewing 八要素就能够生成了，让这八要素跟原始 cookie ，即
	d:\verify\examples\foobar.c， 发生关联，此 cookie 的 sewing 动作完成。
	
	参数命名提示：
	--src-mapping-pdb 中 pdb 字样暗示，此前缀值是用来匹配 srctool -r xxx.pdb 所列出文件的。
	--src-mapping-svn 中 svn 字样暗示，此前缀值是用来匹配你 svn 沙箱中本地文件全路径的。
	

--src-mapping-from-ini=<inifilepath>,<dirSdkOut>,<[global]>,<examples_dir>,<examples_copyto>
	[可选] since v1.2.
	此是对 --src-mapping-pdb 和 --src-mapping-svn 的延伸，专门针对 Scalacon 2016 设计。
	指定了了此选项， --src-mapping-pdb 和 --src-mapping-svn 就被忽略。
	参数行为：通过分析 <inifilepath> 指定的 INI 文件内容来得到 dirpfxpdb 和 dirpfxsvn 的值。
	.
	增加此参数的缘由：在 Scalacon 2016 的设计中，dirpfxpdb 和 dirpfxsvn 的值需要分析 INI 内容
	才能得到，而这个对于 makefile 是个难事，因此，干脆将这个动作交给 py 去处理好了。

--logfile=<logfile>
	[可选]
	将处理过程写入日志文件 <logfile>，追加写入。

--allow-empty-scan
	[可选]
	指定此参数时，允许 --dir-pdb 指定的目录不存在，或其中没有发现 PDB 文件。
	默认不启用此参数，未扫描到 PDB 文件会报错，退出码非零。

"""

import sys
import getopt
import os
import shutil
import errno
import stat
import re
import subprocess
import tempfile
import ConfigParser
from datetime import datetime
import fnmatch

version = "1.2"

opts = {}

g_dp = ''
g_ds = ''
g_dtco = ''
g_drt = ''
g_dftbr = 'trunk'
g_lrt = False
g_svn_use_export = False

g_logfile = None

g_tracks = {}
	# This is a table mapping [cookie] to track
	# Even if a cookie does not have corresponding svn info, it is recorded as well(as None)
	# to avoid checking that cookie with 'svn info' again and again.
g_nSourceFilesFound = 0
	# For those files reported by 'srctool -r', how many of them are actually found
	# from g_ds directory.
g_nValidTracks = 0
	# Total source files listed from 'srctool -r' that results in a track.
	# Note: A source file can result in a valid track when he has correct 'svn info' and the
	#    svn info can be successfully dissected into svnrooturl, reposie and branchie.
	# This count does not count duplicate files indicated by different pdbs.
	# g_nValidTracks must not be greater than g_nSourceFilesFound.
g_nTracksSewed = 0
	# This is the sewing count. If a track is sewed sewed into two pdbs, then the count is two.
	# So g_nTracksSewed>=g_nValidTracks
g_nPdbsSewed = 0
	# Total PDB files that are sewed.
g_nPdbsFound = 0
	# Just counts filename-matching PDBs found, not necessarily sewed with valid tracks.

class CSvnHostinfo:
	def __init__(self, rooturl):
		self.rooturl = rooturl
		self.reposie_table = {}

g_reposietable = {}
	# This table maps svnhostid to a CSvnHostinfo class object.
	#  .rooturl is the SVN base url for that SVN host.
	#  .reposie-table is table content from reposie-<svnhostid>.txt

g_save_sstreams_dir = ''
g_pick_cherries = ''
g_pick_sstreams_dirs = ''
g_pick_sstreams_dirs_from_ini = ''
g_pick_sstreams_dir_sdkin = ''
g_nCherryPicks = 0

g_srcmapping_pdb = ''
g_srcmapping_svn = ''

ErrNoFileProcessed = 9

#g_svnhosttable = {}
	# This table maps svnhostid to SVN base URL.
	# See description in --svnhost-table param.

nlssvnhostid='nlssvn'
nlssvnrooturl='https://nlssvn/svnreps'

srctool_exename = 'srctool-wdk7'
	# WDK7's  'srctool -r' returns 0 on success.
	# WDK10's 'srctool -r' returns count of source files printed, so 0 means error.


SRCSRV_stream_template="""
SRCSRV: ini ------------------------------------------------
VERSION=1
INDEXVERSION=2
VERCTRL=Subversion
DATETIME={datetime}
SRCSRV: variables ------------------------------------------
SvnHostId=%var2%
SvnRootUrl=%var3%
SvnReposie=%var4%
SvnBranchie=%var5%
SvnInnard=%var6%
SvnCoTimeStamp=%var7%
SvnCoTsCompact=%var8%
PirLocal=%SvnCoTsCompact%/%SvnHostId%/%SvnReposie%
DirLocal=%targ%/%PirLocal%
SvnCoCmd=svn.exe co %SvnRootUrl%/%SvnReposie%/%SvnBranchie%@"{{%SvnCoTimeStamp%}}" "%fnbksl%(%DirLocal%)"
SvnExportCmd=svn.exe export --force %SvnRootUrl%/%SvnReposie%/%SvnBranchie%@"{{%SvnCoTimeStamp%}}" "%fnbksl%(%DirLocal%)"
SRCSRVTRG=%fnbksl%(%DirLocal%/%SvnInnard%)
SRCSRVCMD_CHECKOUT=cmd /c %SvnCoCmd% && echo %SvnCoCmd% > "%fnbksl%(%DirLocal%/_svncmd.txt)"
SRCSRVCMD_EXPORT=cmd /c %SvnExportCmd% && echo %SvnExportCmd% > "%fnbksl%(%DirLocal%/_svncmd.txt)"
SRCSRVCMD=%{svncmd}%
SRCSRV: source files ---------------------------------------
{tracks}
SRCSRV: end ------------------------------------------------
"""
	# Variables: {datetime} {svncmd} {tracks}
	# Python hint: the doubling {{ and }} are escape signatures, that is, {{ represents a single { .

def Log(s):
	if g_logfile:
		g_logfile.write(s+'\n')

def Logp(s):
	print s
	if g_logfile:
		g_logfile.write(s+'\n')

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

def FileWriteStr(fname, s, isAppend=False):
	"""
	Create file with name #fname and write string #s to that file.
	If #fname exists, overwrite or append to it(according to isAppend).
	If directory of #fname does not exist, we'll create it.

	Return True or False
	"""
	dir = os.path.dirname(fname)
	if not dir: dir = '.'

	if not os.path.isdir(dir):
		if os.path.exists(dir):
			return False # dir may be a existing file
		try:
			os.makedirs(dir)
		except:
			return False

	# #dir should have been created here.
	try:
		f = open(fname, "ab" if isAppend else "wb")
		f.write(s)
		f.close()
	except:
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

def AssertMissingOpt(reqopts):
	global opts
	# reqopts can be '--xxx=' or '--xxx'
	reqoptschk = [ '--'+(opt[:-1] if opt[-1]=='=' else opt) for opt in reqopts]
	for opt in reqoptschk:
		if not opt in opts:
			print 'Error: No %s option assigned.'%(opt)
			return False
	return True

def ComparePathStr(s1, s2):
	"""
	Compare s1 and s2 as path string,
	* case insensitive
	* path separator '/' and '\' consider the same
	"""
	s1 = s1.lower().replace('\\', '/')
	s2 = s2.lower().replace('\\', '/')
	return True if s1==s2 else False


class Track: pass

def MatchSvnHostId(svnurl):
	for svnhost in g_reposietable.keys():
		if svnurl.find(g_reposietable[svnhost].rooturl)==0 :
			return svnhost
	return ''

def GetSvnRootUrl(svnhostid):
	if svnhostid in g_reposietable:
		return g_reposietable[svnhostid].rooturl
	else:
		return ''

def DissectSvnRemain(svnhostid, urm):
	"""
	Currently, the func not allow to fail, may allow in future
	"""
	svnrooturl = GetSvnRootUrl(svnhostid)

	"""
	>>> svnhostid sample:

	nlssvn

	>>> svnrooturl sample:

	https://nlssvn/svnreps

	>>> urm sample:

 	Isyslib/IUartBasic/dev/libsrc/mswin/UartBasic_win.cpp

	"""

	fntable = ''
	entries = [] # entries in reposie table
	if g_drt:
		fntable = g_drt+'/reposie-'+svnhostid+'.txt'

	rtable = g_reposietable[svnhostid].reposie_table
		# just make a reference with a short name

	if not rtable and g_drt:
		# This table is not initialized yet, now load it from file to form a concrete rtable.

		# Open reposie mapping table according to svnhostid
		try:
			ftable = open(fntable, 'r')
			entries = ftable.read().splitlines()
			ftable.close()
			""" entries sample:
			Isyslib/IUartBasic	gpbr_071126_IUartBasic
			CommonLib/gadgetlib	gpbr_080812_gadgetlib
			CommuLib/1snc	gpbr_080722_1snc
			"""
		except:
			# (note: we keep fntable's value here)
			pass

		for e in entries:
			t = e.split()
			if len(t)==0:
				continue # skip blank line

			gpbr = ''
			reposie = t[0] # sample: 'Isyslib/IUartBasic'
			branchie = g_dftbr # assume 'trunk' first
			if len(t)>1 :
				gpbr = t[1] # sample: 'gpbr_071126_IUartBasic'
				if gpbr in os.environ: branchie = os.environ[gpbr]

			rtable[reposie] = (gpbr, branchie)
			# rtable will have reposie(e.g. 'Isyslib/IUartBasic') as index and
			# a tuple as corresponding value.
			# tuple[0] is gpbr (null if it does not appear in reposie table file)


	for reposie in rtable.keys():
		# Skip this entry if t[0] does not match start of urm
		if urm.find(reposie+'/')!=0 :
			continue

		gpbr = rtable[reposie][0]     # [0]: gpbr
		branchie = rtable[reposie][1] # [1]: branchie

		# Check if branchie match that in the urm, assert error if not
		reposie_branchie_expect = reposie+'/'+branchie+'/'
		if urm.find(reposie_branchie_expect)!=0 : # not match
			Logp("Error: gpbr env(%s) indicates the URL should start with %s/%s , "
				"however, svn info tells %s/%s ." % (
				gpbr if gpbr else 'null',
				svnrooturl, reposie_branchie_expect,
				svnrooturl, urm
				))
			exit(3)

		innard = urm[len(reposie_branchie_expect):]
		return (reposie, branchie, innard)
		""" sample:
		('Isyslib/IUartBasic' , 'dev' , 'libsrc/mswin/UartBasic_win.cpp')
		"""

	# reposie definition not found in reposie table
	if g_lrt:
		# Now we carry out the loosy search method
		""" sample:
		For:
			urm = Isyslib/IUartBasic/trunk/libsrc/mswin/UartBasic_win.cpp
			default-branchie = trunk
		we get:
			reposie = Isyslib/IUartBasic
			branchie = trunk
		"""
		_br_ = '/'+g_dftbr+'/'
		pos = urm.find(_br_)
		if pos>0:
			reposie = urm[0:pos]
			branchie = g_dftbr
			innard = urm[pos+len(_br_):]
			return (reposie, branchie, innard)
		else:
			if fntable:
				Logp(
					"Error: Expected reposie table file '%s' is empty or cannot be opened, and reposie cannot be deduced from loosy method,\n"
					"- for SVN root URL: %s\n"
					"- default branchie: %s\n" \
						%(fntable, svnrooturl, g_dftbr)
					)
				exit(3)
			else:
				Logp(
					"Error: Expected reposie table directory not assigned, and reposie cannot be deduced from loosy method,\n"
					"- for SVN root URL: %s\n"
					"- default branchie: %s\n" \
						%(svnrooturl, g_dftbr)
					)
				exit(3)
	else:
		# Since not g_lrt, we have to assert error.
		Logp(
			"Error: No reposie definition can be found in file %s ,\n"
			"- for SVN root URL: %s\n"
			"- SVN remain parts: %s\n" \
			%(fntable,
			svnrooturl,
			urm
			))
		exit(3)


def CalTrack(cookie):
	"""
	Return the track info(in Track object) corresponding to the input cookie.
	Return None if no track info is available(when the cookie has no svn info).
	
	A cookie is a line in "srctool -r xxx.pdb"'s output, that is one local source filepath
	associated with the pdb.
	
	"""
	# Execute 'svn info' to get the svnurl of that cookie.
	
	if g_srcmapping_pdb and g_srcmapping_svn:
		cookie_l = cookie.lower()
		srcmapping_pdb_l = g_srcmapping_pdb.lower()
		# Check if we should map back to the "real" cookie expected by user.
		if cookie_l.startswith(srcmapping_pdb_l):
			cookie = cookie_l.replace(srcmapping_pdb_l, g_srcmapping_svn, 1)
#			print '>>>>>>>> For cookie "%s", "%s" is replaced with "%s"'%(cookie, g_srcmapping_pdb, g_srcmapping_svn) #debug
	
	svninfo_cmd = 'svn info '+cookie
	try:
		svninfo = subprocess.check_output(svninfo_cmd, stderr=subprocess.STDOUT)
	except WindowsError:
		Logp("Error: 'svn info' execution fail! Perhaps svn.exe is not in your PATH.")
		exit(2)
	except subprocess.CalledProcessError as cpe:
		Log("Warning: '%s' returns error code %d. 'svn info' output:\n%s\n"%\
			(svninfo_cmd, cpe.returncode , cpe.output))
		# This should not be a fatal error, e.g, You can see .res file here.
		# .res is not what we will check into svn.
		return None

	# 'svn info' output sample:
	"""
	Path: G:\w\Isyslib\IUartBasic\libsrc\mswin\UartBasic_win.cpp
	Name: UartBasic_win.cpp
	URL: https://nlssvn/svnreps/Isyslib/IUartBasic/dev/libsrc/mswin/UartBasic_win.cpp
	Repository Root: https://nlssvn/svnreps/Isyslib/IUartBasic
	Repository UUID: e2a01708-1c17-0410-987a-8dc3766a8521
	Revision: 285
	Node Kind: file
	Schedule: normal
	Last Changed Author: chj
	Last Changed Rev: 278
	Last Changed Date: 2011-06-08 15:34:03 +0800 (Web, 2011-06-08)
	Text Last Updated: 2011-06-10 10:17:01 +0800 (Fri, 2011-06-10)
	Checksum: 236f48bf195c1f5c4c83c75762d06c78
	"""
	#    ------------------------- svninfo.replace('\r\r\n', '\r\n') # I don't know why I got \r\r\n
	# We go find the 'URL:' line and get the SVNURL
	r = re.search(r'URL: +(.+)$', svninfo, re.MULTILINE)
	if r:
		svnurl= r.group(1).strip() # svnurl is '\r' terminated, strange
		Log(svninfo)
	else:
		Logp("Error: 'svn info' output unexpected. Cannot find 'URL:' line in the output.")
		Logp("'svn info' output is:\n%s\n"%(svninfo))
		exit(2)

	""" svnurl sample:
	https://nlssvn/svnreps/Isyslib/IUartBasic/dev/libsrc/mswin/UartBasic_win.cpp
	"""

	svnhostid = MatchSvnHostId(svnurl)
	if not svnhostid:
		Logp( "Error: Cannot find matching SVN host id for '%s' whose SVN URL is '%s' ,"
			"-- your svn host table does not provide matching info for that SVN URL."%(cookie, svnurl) )
		exit(5)

	svnrooturl = GetSvnRootUrl(svnhostid)

	svnurl_remain = svnurl[len(svnrooturl)+1:]
	""" svnurl_remain sample:
	Isyslib/IUartBasic/dev/libsrc/mswin/UartBasic_win.cpp
	"""

	r = DissectSvnRemain(svnhostid, svnurl_remain)
	if not r:
		return None

	t = Track()
	t.svnurl = svnurl # This is not a must, only for ease debugging
	t.SvnHostId = svnhostid
	t.SvnRootUrl = svnrooturl
	t.Reposie = r[0]
	t.Branchie = r[1]
	t.Innard = r[2]

	return t

def TimeStampForVar8(s):
	# s sample: "2011-08-29 08:30:00"
	# output sampel: "20110829.083030"
	s = s.replace('-', '')
	s = s.replace(':', '')
	s = s.replace(' ', '.')
	return s

def Sew1Cookie(cookie):
	# Return a track line(a line of text in pdb SRCSRV stream) for cookie

	global g_nValidTracks, g_nTracksSewed

	Log("Sewing source file: %s ..."%cookie)

	if cookie in g_tracks:
		t = g_tracks[cookie]
		Log( "'%s' already in cache%s."%(cookie, '' if t else '(None)') )
	else:
		t = CalTrack(cookie)
		g_tracks[cookie] = t
			# Add the new cookie to cache(even if None). Yes, use filepath as g_tracks' index
		if t:
			g_nValidTracks += 1

	if not t:
		return ''

	g_nTracksSewed += 1

	# concatenate track properties into a track line
	s = cookie # %var1%
	s += '*'+t.SvnHostId # %var2%
	s += '*'+t.SvnRootUrl # %var3%
	s += '*'+t.Reposie # %var4%
	s += '*'+t.Branchie # %var5%
	s += '*'+t.Innard # %var6%
	s += '*'+g_dtco      # %var7%
	s += '*'+TimeStampForVar8(g_dtco) # %var8%
	return s

def append_sstracks_from_streamstxt(ssdict, sstreamtxt):
	# This function modifiies ssdict(a python dict) object.
	with open( sstreamtxt, "rb" ) as f:
		sstream = f.read()
#		print '{{{%s}}}'%(sstream_text_pick) #debug
		r = re.search(
			r'SRCSRV: source files ---+\n(.+)SRCSRV: end ---',
			sstream, re.DOTALL) # let (.+) match multiple lines
		if not r:
			Logp( 'Unexpected: No "SRCSRV: source files" section found in %s. Skipped.\n'%(filename_pick) )
			exit(12)
		
		sstracks = r.group(1)
#		print "[[[cherry-pick(%d)=%s]]]"%(g_nCherryPicks, pick_text) #debug
		for track in sstracks.splitlines():
			if not track in ssdict:
				ssdict[track] = 1
		

def get_pick_sstreams_dirs():
	if g_pick_sstreams_dirs:
		return g_pick_sstreams_dirs.split(",")
	
	if not g_pick_sstreams_dirs_from_ini:
		Logp( 'Error: You request sstreams picking, but does not provide picking dirs.' )
		exit(13)
	
	"""
	For each non-[global] sections, collect cidvers= keys's values as pickdirs.
	Example:
# === INI content start ===
[global]
...

[compiler-id.msvc]
cidvers=vc100x64 vc80
...

[compiler-id.wince]
cidvers=vc80ppc
# === INI content end ===
	and g_pick_sstreams_dir_sdkin='d:/wk/sdkin' , then wet get result:
	[ 'd:/wk/sdkin/vc100x64', 'd:/wk/sdkin/vc80', 'd:/wk/sdkin/vc80ppc' ]
	"""
	allvers = []
	iniobj = ConfigParser.ConfigParser()
	iniobj.read(g_pick_sstreams_dirs_from_ini)
	cid_sections = [ s for s in iniobj.sections() if s.startswith('compiler-id.')]
	for section in cid_sections:
		try:
			cidvers = iniobj.get(section, 'cidvers') # cidvers is space separated 
		except NoOptionError:
			continue # it's abnormal, not likely to happen, neglect it for simplicity
		allvers.extend(cidvers.split())
	
	assert g_pick_sstreams_dir_sdkin
	return [ g_pick_sstreams_dir_sdkin+'/'+v for v in allvers ]

def cherry_pick_srcsrv_tracks(pdbpath):
	
	global g_nCherryPicks 
	print '  Sstream cherry picking for %s ...'%(pdbpath)
	sstracks_all_dict = {} # use python dict as a easy duplication eliminator
	
	try:
		dirs = get_pick_sstreams_dirs()
		for i,dir in enumerate(dirs):
			if dir[0]=='!': # starting with !, then it's a dir relative to pdbpath
				dirs[i] = os.path.join(os.path.split(pdbpath)[0], dir[1:])
			dirs[i] = os.path.abspath(dirs[i])
		# Now dirs[] are all abspath.
		
		if g_pick_cherries=='*':
			# draw in all .sstream.txt found. 
			for dir in dirs:
				if not os.path.isdir(dir):
					continue # ignore non-existing dir
				filenames = os.listdir(dir)
				for filename in filenames:
					if filename.endswith('.sstream.txt'):
						sstream_filepath = dir+'/'+filename
						print '  > picking from %s'%(sstream_filepath)
						append_sstracks_from_streamstxt(sstracks_all_dict, sstream_filepath)
						g_nCherryPicks += 1
		else:
			# looks for specific <cherry>.sstream.txt files
			cherries = g_pick_cherries.split(',')
			for cherry in cherries:
				sstracks = ''
				for dir in dirs:
					if not os.path.isdir(dir):
						continue # ignore non-existing dir
					sstream_filepath = dir+'/'+ "%s.sstream.txt"%(cherry)
					if os.path.isfile(sstream_filepath):
						print '  > picking from %s'%(sstream_filepath)
						append_sstracks_from_streamstxt(sstracks_all_dict, sstream_filepath)
						g_nCherryPicks += 1
						# break // just go on and pick from all dirs
				
				if not sstracks:
					Logp( 'Error: You assign %s in --pick-cherries, but %s.sstream.txt cannot be found.'%(cherry, cherry) )
					exit(11)

	except IOError:
		# PENDING: Wish a more elegant way to know the error file.
		Logp( "Error: IOError on %s."%(sstream_filepath) )
		exit(10)

	return '\n'.join(sstracks_all_dict.keys())

def Sew1Pdb(pdbpath):
	pdbpath = os.path.abspath(pdbpath) # pdb filepath
	
	srctool_cmd = '%s -r "%s"'%(srctool_exename, pdbpath)
	Log("\nStart sewing PDB: %s"%pdbpath)

	try:
		srclist_ = subprocess.check_output(srctool_cmd)
	except WindowsError:
		Logp("Error: '%s -r' execution fail! Perhaps %s.exe is not in your PATH."%(srctool_exename, srctool_exename))
		exit(1)
	except subprocess.CalledProcessError as cpe:
		Logp("Error: '%s' returns: %s\n"%(srctool_cmd, cpe.output))
		exit(1)

	srclist = srclist_.split()

	""" srclist sample:
    g:\w\isyslib\iuartbasic\libsrc\mswin\uartbasic_win.cpp
	g:\w\commonlib\common-include\mswin\mswinclarify.h
	g:\w\isyslib\iuartbasic\libsrc\iuartbasic_common.cpp
	o:\nls-build-env\compilers\vs2005\vc\platformsdk\include\basetsd.h
	o:\nls-build-env\compilers\vs2005\vc\platformsdk\include\winerror.h
    f:\sp\vctools\crt_bld\self_x86\crt\src\wchtodig.c
	f:\sp\vctools\crt_bld\self_x86\crt\src\atox.c
	"""

	# filter the source files we want(those inside --dir-source)
	srclist_want = filter( lambda s : ComparePathStr(g_ds, s[0:len(g_ds)]) , srclist)

	""" srclist_want sample, when g_ds="g:\w" :
    g:\w\isyslib\iuartbasic\libsrc\mswin\uartbasic_win.cpp
	g:\w\commonlib\common-include\mswin\mswinclarify.h
	g:\w\isyslib\iuartbasic\libsrc\iuartbasic_common.cpp
	"""

	global g_nSourceFilesFound, g_nCherryPicks
	g_nSourceFilesFound += len(srclist_want)

	tracks_self = '' # store tracks text
	tracks_pick = '' # store tracks text 
	tracks_all = ''  # store tracks text 
	ntrack = 0

	for cookie in srclist_want:
		t = Sew1Cookie(cookie)
		if t:
			tracks_self += t+'\n'
			ntrack+=1

	if ntrack==0 and not g_pick_cherries:
		return True # Do nothing more and return

	if g_pick_cherries:
		tracks_pick = cherry_pick_srcsrv_tracks(pdbpath)
	
	tracks_all = tracks_self + '\n' + tracks_pick
	
	srcsrv_stream_text = SRCSRV_stream_template.format(
		datetime=g_dtco,
		tracks=tracks_all,
		svncmd='SRCSRVCMD_EXPORT' if g_svn_use_export else 'SRCSRVCMD_CHECKOUT'
		)

	fstream = tempfile.NamedTemporaryFile(delete=False)
	if fstream:
		fnstream = fstream.name
		Log( "Created temp file '%s' for SRCSRV stream."%fnstream )
		fstream.write(srcsrv_stream_text)
		fstream.close()
	else:
		Logp( "Error: Cannot create a temp file to store SRCSRV stream." )
		exit(4)

	Log( "SRCSRV stream tracks: %d. SRCSRV stream is:\n%s\n"%(ntrack, srcsrv_stream_text) )

	# call pdbstr.exe to embed the SRCSRV stream
	pdbstr_cmd = 'pdbstr -w -p:"%s" -i:"%s" -s:srcsrv'%(pdbpath, fnstream)
	Log( "Embedding SRCSRV stream into %s ..."%pdbpath )
	try:
		subprocess.check_output(pdbstr_cmd, stderr=subprocess.STDOUT)
	except WindowsError:
		Logp("Error: 'pdbstr' execution fail! Perhaps pdbstr.exe is not in your PATH. You should install Debugging Tools for Windows to obtain it.")
		exit(4)
	except subprocess.CalledProcessError as cpe:
		Logp( "%s\n"%cpe.output )

	""" True case of a generated SRCSRV stream. You can view it by running ``pdbstr -r -p:IUartBasic.pdb -s:srcsrv''
	This is named srcsrv_stream_text or sstream_text below.
	
	SRCSRV: ini ------------------------------------------------
	VERSION=1
	INDEXVERSION=2
	VERCTRL=Subversion
	DATETIME=2011-09-21 16:21:21
	SRCSRV: variables ------------------------------------------
	SvnHostId=%var2%
	SvnRootUrl=%var3%
	SvnReposie=%var4%
	SvnBranchie=%var5%
	SvnInnard=%var6%
	SvnCoTimeStamp=%var7%
	SvnCoTsCompact=%var8%
	PirLocal=%SvnCoTsCompact%/%SvnHostId%/%SvnReposie%
	DirLocal=%targ%/%PirLocal%
	SvnCoCmd=svn.exe co %SvnRootUrl%/%SvnReposie%/%SvnBranchie%@"{%SvnCoTimeStamp%}" "%fnbksl%(%DirLocal%)"
	SvnExportCmd=svn.exe export --force %SvnRootUrl%/%SvnReposie%/%SvnBranchie%@"{%SvnCoTimeStamp%}" "%fnbksl%(%DirLocal%)"
	SRCSRVTRG=%fnbksl%(%DirLocal%/%SvnInnard%)
	SRCSRVCMD_CHECKOUT=cmd /c %SvnCoCmd% && echo %SvnCoCmd% > "%fnbksl%(%DirLocal%/_svncmd.txt)"
	SRCSRVCMD_EXPORT=cmd /c %SvnExportCmd% && echo %SvnExportCmd% > "%fnbksl%(%DirLocal%/_svncmd.txt)"
	SRCSRVCMD=%SRCSRVCMD_EXPORT%
	SRCSRV: source files ---------------------------------------
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\mswin\uartbasic_create.cpp*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/mswin/UartBasic_create.cpp*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\include\iuartbasic\iuartbasic_mswin_spi.h*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/include/IUartBasic/IUartBasic_mswin_spi.h*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\commonlib\common-include\commdefs.h*nlssvn*https://nlssvn/svnreps*CommonLib/common-include*dev*commdefs.h*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\include\iuartbasic\iuartbasic.h*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/include/IUartBasic/IUartBasic.h*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\include\uartbasic_win.h*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/include/UartBasic_win.h*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\mswin\uartbasic_win.cpp*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/mswin/UartBasic_win.cpp*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\commonlib\common-include\mswin\mswinclarify.h*nlssvn*https://nlssvn/svnreps*CommonLib/common-include*dev*mswin/mswinClarify.h*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\mswin\iuartbasic-winver.h*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/mswin/iuartbasic-winver.h*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\iuartbasic_common.cpp*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/IUartBasic_common.cpp*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\c_iuartbasic.cpp*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/C_IUartBasic.cpp*2011-09-21 16:21:21*20110921.162121
	d:\nlsbuild\nlssdk\nlssdk-v0.3\msvc-sdk\nlssdk-msvc-v0.3-src\isyslib\iuartbasic\libsrc\include\iuartbasic\c_iuartbasic.h*nlssvn*https://nlssvn/svnreps*Isyslib/IUartBasic*dev*libsrc/include/IUartBasic/C_IUartBasic.h*2011-09-21 16:21:21*20110921.162121
	SRCSRV: end ------------------------------------------------
	"""
	
	if g_save_sstreams_dir:
		save_sstream_as_file(srcsrv_stream_text, pdbpath)

	try:
		os.remove(fnstream)
	except:
		Log( "Warning: Unable to delete temp file '%s'."%fnstream )
		# not fatal

	global g_nPdbsSewed
	g_nPdbsSewed +=1

	return True


def ScanAndSew():
	"""
	g_dp, g_ds, g_drt, g_dtco as input params
	
	[2016-03-06] For .lib.pdb, 'srctool -r' shows nothing(Microsoft did it deliberately), 
	so we don't have to bother with *.lib.pdb .
	"""
	for root, folders, files in os.walk(g_dp):
		# In files, search for *.pdb but not *.lib.pdb
		for file in files:
			if fnmatch.fnmatch(file, '*.pdb') and not fnmatch.fnmatch(file, '*.lib.pdb'):
				global g_nPdbsFound
				g_nPdbsFound += 1
				Sew1Pdb(root+'/'+file)

	return True


def save_sstream_as_file(sstream_text, pdbpath):
	# Save the sstream text, we'll use it creatively for static .libs.
	pdbdir, pdbfilename = os.path.split(pdbpath)
	sstream_stemname = pdbfilename.rstrip(".pdb").rstrip(".lib")

	if g_save_sstreams_dir[0]=='!':
		save_filepath = "%s/%s/%s.sstream.txt"%(pdbdir, g_save_sstreams_dir[1:], sstream_stemname)
	else:
		save_filepath = g_save_sstreams_dir

	save_filepath = os.path.abspath(save_filepath)

	Logp("  Saving sstream file: %s"%(save_filepath) )
	with open(save_filepath, "wb+") as f:
		f.write(sstream_text)



def main():
	global opts, g_dp, g_ds, g_dtco, g_drt, g_dftbr, g_lrt
	global g_logfile, g_svn_use_export
	global g_save_sstreams_dir, g_pick_cherries, g_pick_sstreams_dirs
	global g_pick_sstreams_dirs_from_ini, g_pick_sstreams_dir_sdkin
	global g_srcmapping_pdb, g_srcmapping_svn

	reqopts = ['dir-pdb=', 'dir-source=', 'datetime-co=', 'svnhost-table=' ]
	optopts = [
		'svn-use-export', 'logfile=', 'default-branchie=',
		'dir-reposie-table=', 'loosy-reposie-table', 
		'save-sstreams-dir=', 'pick-cherries=', 'pick-sstreams-dirs=', 
		'pick-sstreams-dirs-from-ini=', 'pick-sstreams-dir-sdkin=',
		'src-mapping-pdb=', 'src-mapping-svn=', 'src-mapping-from-ini=',
		'allow-empty-scan', 'version'] # optional arguments
	optlist,arglist = getopt.getopt(sys.argv[1:], '', reqopts+optopts)
	opts = dict(optlist)

	if '--version' in opts:
		print '%s v%s'%(os.path.basename(__file__), version)
		return 0

	if not AssertMissingOpt(reqopts):
		return 1

	g_dp = opts['--dir-pdb']
	g_ds = opts['--dir-source']

	if '--dir-reposie-table' in opts:
		g_drt = opts['--dir-reposie-table']

	if '--loosy-reposie-table' in opts:
		g_lrt = True
	else:
		if not g_drt:
			print "Error: You must provide --dir-reposie-table=<drt> option unless you specify --loosy-reposie-table."
			return 1

	g_dtco = opts['--datetime-co']
	if g_dtco=='now':
		g_dtco = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	if '--svn-use-export' in opts:
		g_svn_use_export = True

	if '--default-branchie' in opts:
		g_dftbr = opts['--default-branchie']

	if '--save-sstreams-dir' in opts:
		g_save_sstreams_dir = opts['--save-sstreams-dir']

	if '--pick-cherries' in opts:
		g_pick_cherries = opts['--pick-cherries']

	if '--pick-sstreams-dirs-from-ini' in opts:
		g_pick_sstreams_dirs_from_ini = opts['--pick-sstreams-dirs-from-ini']
		if '--pick-sstreams-dir-sdkin' in opts:
			g_pick_sstreams_dir_sdkin = opts['--pick-sstreams-dir-sdkin']
		else:
			Logp( 'Error: You assign --pick-sstreams-dirs-from-ini but missing --pick-sstreams-dir-sdkin .' )
			exit(1)
	elif '--pick-sstreams-dirs' in opts:
		g_pick_sstreams_dirs = opts['--pick-sstreams-dirs']

	if g_pick_cherries and not (g_pick_sstreams_dirs or g_pick_sstreams_dirs_from_ini):
		Logp('Error: You assign --pick-cherries but no --pick-sstreams-dirs. You have to fix it.')
		exit(1)

	if '--src-mapping-from-ini' in opts:
		inipath, dir_sdkout, _section_, key_src_mapping_pdb, key_src_mapping_svn = \
			opts['--src-mapping-from-ini'].split(",")
		section = _section_.strip('[]') # turns '[global]' into 'global'
		iniobj = ConfigParser.ConfigParser()
		iniobj.read(inipath)
		try:
			g_srcmapping_pdb = dir_sdkout +'/'+ iniobj.get(section, key_src_mapping_pdb)
			g_srcmapping_svn = os.path.join(os.path.split(inipath)[0], iniobj.get(section, key_src_mapping_svn))
		except ConfigParser.NoOptionError as e:
			Logp( 'Scalacon info: Your --src-mapping-from-ini= option is ignored, because the INI does not have "[%s] %s=..." assignment.'%(e.section, e.option) )
			pass
	else:
		if '--src-mapping-pdb' in opts:
			g_srcmapping_pdb = opts['--src-mapping-pdb'].replace('/', '\\')
		if '--src-mapping-svn' in opts:
			g_srcmapping_svn = opts['--src-mapping-svn'].replace('/', '\\')

	g_srcmapping_pdb = os.path.abspath(g_srcmapping_pdb) if g_srcmapping_pdb else ''
	g_srcmapping_svn = os.path.abspath(g_srcmapping_svn) if g_srcmapping_svn else ''
		# Note: os.path.abspath("") will return abspath of current working directory.
#@#
	if g_srcmapping_pdb and g_srcmapping_svn:
		print 'Assign srcmapping:\n  prefix-in-pdb: %s\n  prefix-in-svn: %s\n'%(g_srcmapping_pdb, g_srcmapping_svn)
	
	is_allow_empty_scan = True if '--allow-empty-scan' in opts else False
	
	if '--logfile' in opts:
		fnlog = opts['--logfile']
		try:
			os.mkdir(os.path.dirname(fnlog))
		except:
			pass # Leave error to open() below

		try:
			g_logfile = open(fnlog, "ab")
		except:
			print "Error: Cannot open logfile '%s' for write."%(opts['--logfile'])
			exit(1)
		# Log current time
		Log( "\n[%s]"%(datetime.now()) )
		# Log command parameters
		Log( sys.argv[0] )
		for i in range(1 ,len(sys.argv)):
			Log( "\t%s"%(sys.argv[i]) )

	# Assert valid directories
	for d in [g_dp, g_ds] + ([g_drt] if g_drt else []):
		if not os.path.isdir(d):
			print "Error: Your input directory '%s' (abspath: %s) does not exist!"%(d, os.path.abspath(d))
			return 2

	g_ds = os.path.abspath(g_ds)
		# No need to translate other paths to abs.

	# Fetch SVN host table from file.
	svnhosttable_buf = ''
	fnSvnhostTable = opts['--svnhost-table']
		# Two cases: 1. it's a local file, 2. it's an SVN url.
	if ':' in fnSvnhostTable[2:]: # so it may be http://... https://... instead of C:\... ,D:\... etc
		# Process as an SVN url. svn cat that file to current dir.
		flocal = fnSvnhostTable.split('/')[-1]
		try:
			svn_cat_cmd = "svn cat %s"%(fnSvnhostTable)
			svnhosttable_buf = subprocess.check_output(svn_cat_cmd)
		except WindowsError:
			Logp( "Error: '%s' execution fail! Probably you don't have svn.exe in your PATH."%(svn_cat_cmd) )
			exit(1)
		except subprocess.CalledProcessError as cpe:
			Logp( "Error: '%s' execution fail, exit code is %d. Output is:\n%s"%(
				svn_cat_cmd, cpe.returncode , cpe.output) )
	else:
		# Process fnSvnhostTable as local file.
		try:
			ftable = open(fnSvnhostTable, 'r')
			svnhosttable_buf = ftable.read()
			ftable.close()
		except:
			Logp( "Error: Cannot open svn host table file '%s' ."%(fnSvnhostTable) )
			exit(1)

	Log( "SVN host table has content:\n%s\n"%(svnhosttable_buf) )

	entries = svnhosttable_buf.splitlines()
	""" entries sample:
	nlssvn	https://nlssvn/svnreps
	chjsvn	http://chjsvn.dev.nls:88
	"""
	if len(entries)==0:
		Logp( "Error: SVN host table has no entries." )
		exit(1)

	for e in entries:
		svnhostid = e.split()[0]
		svnrooturl = e.split()[1]
		g_reposietable[svnhostid] = CSvnHostinfo(svnrooturl)


	b = ScanAndSew()

	if b:
		if g_nValidTracks>0 or g_nCherryPicks>0:
			Logp( "Success!\n"
				"  Valid tracks found: %d\n"
				"  Tracks(self) sewed into PDBs: %d\n"
				"  Cherry picks into PDBs: %d\n"
				"  PDBs sewed: %d\n" % (g_nValidTracks, g_nTracksSewed, g_nCherryPicks, g_nPdbsSewed)
				)
			return 0 # Success
		else:
			prompt = "Scalacon info: " if is_allow_empty_scan else "Scalacon Error: "
			
			if g_nPdbsFound==0:
				Logp( prompt+"No matching PDBs found in input directory '%s' ."%(g_dp))
			elif g_nSourceFilesFound==0:
				Logp( prompt+"For all scanned PDBs, no associating source files is found in '%s' ."%(g_ds))
			else:
				Logp( prompt+"No valid tracks are sewed into any found PDB. "
					"Probably, no source files associated with your PDBs are in any svn sandbox, "
					"so I cannot deduce their SVN URL to form a track."
					)
			return 0 if is_allow_empty_scan else ErrNoFileProcessed
	else:
		return 4

if __name__ == '__main__':
	try:
		ret = main()
	finally:
        # Without this finally, an exit(errorcode) in the half way will cause
		# logging info in cache go lost.
		if(g_logfile):
			g_logfile.close()

	exit(ret)
