#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
为Scalacon系统服务，对一个目录（文件夹）中的子目录名、文件名、以及文本文件内容进行深度改名。

输入参数：

--topdir=<TopDir>
	指出程序运行要进入操作的顶级目录，目录可指定为相对目录或绝对目录，但不能是当前工作目录自身或其父目录。
	在Window环境下，TopDir如果为驱动器盘符，如'E:\'则程序参数'--copy'不能被指定

--oldname=<OldName>
	指出需要被改名的字符串，或以元组或列表的方式提供超过一个的字符串

--newname=<NewName>
	指出改名后的新的字符串，或以元组或列表的方式提供超过一个的字符串。
	新的名字将和旧的名字建立一个字典，所以需要保证新名字的个数不大于旧名字的个数，允许多个旧名字被对应到一个新名字。

--ignore=<Ignore='.svn'>
	指出程序运行是否忽略指定目录，如果忽略指定目录并且'--copy'参数被指定，用户将不对指定目录进行拷贝。默认设置忽略顶级目录下每一级目录的'.svn'目录

--copy
	指出程序运行是否需要保存原顶级目录并建立新顶级目录进行后续操作。默认设置保存，但需要注意顶级目录不能直接为驱动器盘符。

--update-uuid-by-keys=<keys sperated by comma>
	指出一系列需要替换UUID的地方。
	比如：
		--update-uuid-by-keys=ProjectGUID,MyGuid
	将在文件内容中寻找 ProjectGUID 和 MyGuid。拿 ProjectGUID 举例，若找到一行为
		ProjectGUID="{EB2CCB13-1BA8-44CD-B5B7-6FB5921D72D3}"
	则认为 ProjectGUID 对应的 UUID 为 EB2CCB13-1BA8-44CD-B5B7-6FB5921D72D3，接着，生成一个随机的 UUID，
	将所有出现 EB2CCB13-1BA8-44CD-B5B7-6FB5921D72D3 的地方替换为新的 UUID。
	-
	注：
	* 若 ProjectGUID 所在的行里头有两个 UUID 字串，则该程序只处理 ProjectGUID 后的第一个 UUID 字串。
	* 若 ProjectGUID 在一行中出现两次，本程序也仅处理第一个对应的 UUID 数值。
	* 若 ProjectGUID 在多行中出现，本程序也仅处理第一个对应的 UUID 数值
	-
	案例：VS2005 工程文件 .vcproj 中有 UUID，且不同的工程应该带不同的 ProjectGUID，否则加入同一 sln 会出麻烦。

注：程序运行将在硬盘上实现复制和修改的行为，但对于二进制文件，程序允许对二进制文件进行改名，但决不允许修改二进制文件的内容
"""

import sys
import getopt
import datetime
import os
import shutil
import errno
import stat
import uuid
import re
#import ConfigParser
#from Cheetah.Template import Template
import types
version = "1.1"

opts = {}


def UpdateUuidByKey(s, key):
	"""
	#key is a string , e.g. "ProjectGUID"
	"""
	findpos = s.find(key)
	if findpos == -1:
		#print "Warning: no UUID key '%s' found." %(key)
			# This warning should be suppressed, because you should not expect every file in top-dir has that UUID key.
		return s # #key not found, return s as is.
	
	orig_uuid_str = ''
	
	# Split s into lines, and exactly find out which line is it in.
	lines = s.split('\n')
	for line in lines:
		findpos = line.find(key) # TODO: We should Find whole word only!!!
		if findpos == -1:
			continue
		r = re.search(r'\b[A-Fa-f0-9]{8}(?:-[A-Fa-f0-9]{4}){3}-[A-Fa-f0-9]{12}\b', line)
		if r:
			orig_uuid_str = r.group(0)
			break
		else:
			continue

	if not orig_uuid_str:
		print "Warning: No UUID found along side key '%s'." %(key)
		return s
	
	# Generate a new UUID and replace them
	new_uuid_str = str(uuid.uuid1()).upper()
	s = s.replace(orig_uuid_str, new_uuid_str)
	return s
	

def ReplaceContentStr(s, dic):
	for key in dic:
		s = s.replace(key , dic[key])
		
	# Do UUID replace
	if '--update-uuid-by-keys' in opts:
		uuid_keys = opts['--update-uuid-by-keys'].split(',')
		for key in uuid_keys:
			s = UpdateUuidByKey(s, key)
	
	return s

def ReplaceFileStr(s, dic):
	"""

	"""

	l = s.split('.')
	if len(l) == 1:
		return ReplaceContentStr(s, dic)
	else:
		s = '.'.join(l[:-1])
		for key in dic:
			s = s.replace(key , dic[key])

		s = s + '.' + l[-1]
		return s

def ConstituteNewPath(OldPath,NewPath):
	LOP = OldPath.split('\\')
	LNP = NewPath.split('\\')
	LOP = LOP[len(LNP):]
	LNP += LOP
	NewPath = '\\'.join(LNP)

	return NewPath


def IsBinFile(str):
	FileSize = len(str)
	#JudgeLen = FileSize if FileSize < 4096 else 4096
	for i in range(FileSize):
		if 0 <= ord(str[i]) < 9:
			return True
	else:
		return False

def ReName_Folders(root,folders, IsToCopy, CopyTo,dic):

	if IsToCopy == True:
		CopyTo = ConstituteNewPath(root, CopyTo)

	for folder in folders:
		OldAbsPath = os.path.join(root, folder)
		NFolder = ReplaceFileStr(folder,dic)

		if IsToCopy == True:
			NewAbsPath = os.path.join(CopyTo, NFolder)
			try:
				os.mkdir(NewAbsPath)
			except:
				print "Cannot copy tree '%s' to '%s' !" % (OldAbsPath, NewAbsPath)
			else:
				folders.remove(folder)
				folders.append(NFolder)
				print 'copied  : %s -> %s' % (OldAbsPath,NewAbsPath)
		else:
			if NFolder != folder:
				folders.remove(folder)
				folders.append(NFolder)
				print 'Renamed : %s -> %s' % (OldAbsPath,NewAbsPath)

def ReName_ContentInFiles(root,files,IsToCopy, CopyTo,dic):

	if IsToCopy == True:
		CopyTo = ConstituteNewPath(root, CopyTo)

	for file in files:
		OldAbsPath = os.path.join(root, file)
		NFile = ReplaceFileStr(file,dic)

		if IsToCopy == True:
			NewAbsPath = os.path.join(CopyTo, NFile)
			print 'copied  : %s -> %s' % (OldAbsPath,NewAbsPath)
		else:
			if NFile != file:
				try:
					NewAbsPath = os.path.join(root, NFile)
					os.renames(OldAbsPath, NewAbsPath)
					print 'Renamed : %s -> %s' % (OldAbsPath,NewAbsPath)
					OldAbsPath = NewAbsPath  #the true OldAbsPath is not exit because rename has went into effect
				except:
					print "Error:ReName Failed!"
			else:
				NewAbsPath = OldAbsPath #OldAbsPath no change,so NewAbsPath is the same to OldAbsPath,the NewAbsPath is about to be used

		f=open(OldAbsPath,'rb')
		Contents =''
		Contents = f.read()
		f.close()
		if not IsBinFile(Contents):
			NewContents = ReplaceContentStr(Contents,dic)
			if NewContents != Contents:
				print 'Replaced: %s' % NewAbsPath
		else:
			NewContents = Contents
			print 'Bin File: %s' % NewAbsPath
		f=open(NewAbsPath,'wb')
		f.write(NewContents)
		f.close()
	else:
		return True

def Scalacon_Deep_Rename(TopDir,OldName,NewName,IsToCopy,Ignore='.svn'):
	DicReName={}
	if type(OldName) is types.StringType and type(NewName) is types.StringType:
		DicReName[OldName] = NewName
		#print 'DicReName{} init ok'
	elif type(OldName) is types.TupleType:
		for i in OldName:
		   DicReName[i] = NewName if type(NewName) is types.StringType else NewName[0]
		#else:
			#print 'DicReName{} init ok'

	if not os.path.isdir(TopDir):
			print "Error!!!: '%s' is not an existing directory!" % TopDir
			return 1
			
	NTopDir = ReplaceContentStr(TopDir,DicReName)

	if IsToCopy == True:
		if NTopDir == TopDir:
			NTopDir += '.' + NewName

		try:
			os.mkdir(NTopDir)
			print 'Renamed : %s -> %s' % (TopDir,NTopDir)
		except:
			print "Cannot copy tree '%s' to '%s' !" % (TopDir, NTopDir)
			return

		#else:
			#continue next step

	#print 'begin os.walk(%s)' % TopDir
	for root, folders, files in os.walk(TopDir):
		if Ignore == '.svn':
			if '.svn' in folders:
				folders.remove('.svn')
		else:
			if Ignore in folders:
				folders.remove(Ignore)
		ReName_ContentInFiles(root,files,IsToCopy, NTopDir,DicReName)
		ReName_Folders(root,folders,IsToCopy, NTopDir,DicReName)
	else:
		print 'Finished!'


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
	global opts #, dirTmpl, dirNlssvn, rirRepo
	By_Raw_Input = False
	reqopts = ['topdir=', 'oldname=', 'newname=']
	optlist,arglist = getopt.getopt(sys.argv[1:], '',
		['topdir=', 'oldname=', 'newname=', 'copy', 'update-uuid-by-keys=', 'version'])
	for opt in optlist:
		opts[opt[0]] = opt[1]

	if '--version' in opts:
		print os.path.realpath(__file__),version
		return 0

	if not AssertMissingOpt(reqopts):
		print 'type opt by raw_input'

		TopDir = raw_input('type Top-level directory:')
		OldName=raw_input("type old name:")
		NewName=raw_input("type new name:")
		IsToCopy=raw_input("type copy [y]/n?")
		if IsToCopy in ['n','N']:
			IsToCopy = False
		else:
			IsToCopy = True


	else:
		TopDir = opts['--topdir']
		OldName = opts['--oldname']
		NewName = opts['--newname']
		if '--copy' in opts:
			IsToCopy = True
		else:
			IsToCopy = False

#Scalacon_Deep_Rename(TopDir,OldName,NewName,Ignore='.svn',MakeBck = True)

	#print 'Enter Scalacon_Deep_Rename'
	ret=Scalacon_Deep_Rename(TopDir,OldName,NewName,IsToCopy)

	#print os.path.realpath(__file__)
	#print __file__ #和上一行的效果一样，都可以得到可执行程序（自身）的文件名，包括他的存放绝对路径

	#GetSelfInfo = sys._getframe(0).f_code  #返回调用栈信息，包括调用函数名，文件名及行号
	#print "%s (%s @ %d)" % (GetSelfInfo.co_name, GetSelfInfo.co_filename, GetSelfInfo.co_firstlineno)

	if By_Raw_Input == True:
		raw_input("type enter to exit...")


	return 1 if ret else 0

if __name__ == '__main__':
	ret = main()
	exit(ret)
