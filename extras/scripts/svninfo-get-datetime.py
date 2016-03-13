#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分析 svn info 的输出，找出 Last Changed Date 时间戳，将其返回于 stdin 。

唯一的输入参数是一个本地目录名，指出 svn local working copy 的目录，将针对那个目录
查 svn info 。

Require python 2.7 .

svn 1.8.10 ， svn info 输出信息如下：


Path: .
Working Copy Root Path: P:\Scalacon\mm4
URL: https://nlssvn/svnreps/CommonLib/mm_snprintf/trunk/make-sdk/sdk-msvc-all
Relative URL: ^/trunk/make-sdk/sdk-msvc-all
Repository Root: https://nlssvn/svnreps/CommonLib/mm_snprintf
Repository UUID: dc168a7b-aa3d-3042-810d-be3412ed54f5
Revision: 119
Node Kind: directory
Schedule: normal
Last Changed Author: chj
Last Changed Rev: 119
Last Changed Date: 2016-03-05 22:48:02 +0800 (周六, 05 三月 2016)

Note: The datetime format "2016-03-05 22:48:02 +0800" seems to be solid,
i.e. not related to C locale setting. Good!

"""

import os
import sys
import shlex
import subprocess
import re

def main():
	if len(sys.argv)==1:
		sys.stderr.write('Error: A local directory is required to check svn info.')
		return 1
	
	localdir = sys.argv[1]
	
	cmd = 'svn info "%s"'%(localdir)
#	print "zzzzzzz", shlex.split(cmd, posix=False)
	try:
		Output = subprocess.check_output(shlex.split(cmd))
	except OSError as errinfo:
		print "Cannot execute requested command (%s)"%errinfo 
		# errinfo 典型内容之一 "[Error 2] The system cannot find the file specified"
		exit(4)
	except subprocess.CalledProcessError as cpe:
		print "Error: '%s' execution fail, exit code is %d. Output is:\n%s"%(cmd, cpe.returncode , cpe.output)
		exit(5)
	
	r = re.search(r'Last Changed Date: ([0-9\-]+) ([0-9:]+)', Output)
	if r:
		datetime_str = "%s %s"%(r.group(1), r.group(2))
		print datetime_str ,
		return 0
	else:
		sys.stderr.write('Error: Cannot find "Last Changed Date" info from "svn info" output. The searched string is:\n')
		sys.stderr.write(Output)

if __name__ == '__main__':
    ret = main()
    exit(ret)


