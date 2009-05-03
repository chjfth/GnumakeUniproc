[2008-10-24]

The CopyPathExt project is from http://www.codeproject.com/KB/shell/copypathext.aspx .
After ``regsvr32 CopyPathExt.dll'', your explorer will have a new context menu item called
"Copy Path to Clipboard" when right-click on a file fir a folder.

The difference between "MinSize" and "MinDependency" seems lies only in one place,
a compiler flag:
* MinSize: /D "_ATL_DLL"
* MinDependency: /D "_ATL_STATIC_REGISTRY" 

NOTE: Currently, MIDL generated files(.h, .c, .tlb etc) are placed in source file directory, 
therefore, doing a ``rm -fr gf'' will not clean those files, so a second run of umake 
will not call MIDL compiler -- unless you manually delete those MIDL generated files.

Tested with Visual C++ 6 with Platform SDK Feb 2003(Core SDK, Internet Development SDK).


Comment for building with VS2005 or VS2005 SP1, and run it on Windows XP SP2:

* You have to install a Platform SDK(e.g. Platform SDK for Windows Server 2003 R2, March 2006), this PSDK provides the "correct" ComDef.h(different than the one in $VS/VC/include) so that the compiler phase can be done.
	Otherwise, compiler error occurs like this:
	========================
	[cl] ../../CopyPathContextMenu.cpp
	...\CopyPathContextMenu.h(48) : error C2787: 'IContextMenu3' : no GUID has been associated with this object
	...\CopyPathContextMenu.h(48) : error C2440: 'initializing' : cannot convert from 'DWORD_PTR' to 'const IID *'
	... etc ...
	========================
* With correct Platform SDK, linking of CopyPathExt.dll succeeds but running regsvr32 on it fails, error info like this:
	========================
	Runtime Error!
	Program: C:\WINNT\system32\regsvr32.exe
	R6034
	An application has made an attempt to load the C runtime library incorrectly.
	Please contact the application's support team for more information.
	========================
What's more, it still asserts error even if -D_ATL_STATIC_REGISTRY is passed as compile command line.

Solution: According to http://www.grimes.demon.co.uk/workshops/fusWSThirteen.htm referred to by http://www.itwriting.com/blog/?postid=261 , you can run a command like

  mt /manifest CopyPathExt.dll.manifest /outputresource:CopyPathExt.dll;#2

This command embeds the manifest file into the dll, then the resulting CopyPathExt.dll can be done with regsvr32.


[2009-04-06]

I find today that compiling this project on x64 Windows(with VS2005) still fails, even if you have PSDK March 2006 installed. I later find the answer from the comment beneath this codeproject article. The first parameter for GetCommandString should be updated from UINT to UINT_PTR. This solves the x64 building problem.

Also, it seems with that UINT_PTR update, you even don't have to install PSDK March 2006.
