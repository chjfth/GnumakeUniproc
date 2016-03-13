[2010-03-30] Chj:
GnumakeUniproc author places this directory here for convenient working with his company.

- If you're an average GnumakeUniproc user, just ignore this directory.

- If you're an Nlscan staff who would build Nlscan source codes with GnumakeUniproc, you 
  probably need it. Remember, the latest content here may be updated quite constantly. 
  You should always be ready to update it from SVN. The command line is:
    svn export --force https://nlssvn/svnreps/makingsys/GMU-addons/trunk/nlscan/ .

==============================================================================
About the "wince" compiler config here(in "wince" sub-directory)
==============================================================================
The compiler-config-mki files in ./compiler-cfgs/wince is for building ARM based WinCE programs with Microsoft VS2005 compiler.

Using guide:
* To do command line compile of WinCE programs with VS2005 compiler, you have to set compiling environment first(i.e. env-var INCLUDE, LIB, PATH). Unfortunately, VS2005 seems not to provide some stock vcvarsall.bat for WinCE compiler, so I provide vswince.bat as an example(known from VS2005 IDE).
* You should run with umakeU or umakeUD, so that UNICODE & _UNICODE macro is defined. This is normally required by an WinCE program.
* You have to set proper target machine type(gmp_wince_u_MachType) and target machine WinCE version(gmp_wince_u_TargetCeVer) so that proper default compile & link options are selected. 
  For example, use
	umakeU gmp_wince_u_TargetCeVer=0x420 gmp_wince_u_MachType=PPC2003
  to launch a build.

You can use use_PI_always_compile project to test WinCE compile.

NOTE: The compiler-config-mki files here serves only as an working example. In other word, if you want to use a compiler other than the one in VS2005, or you want to compile for X86 or MIPS, you have to tune these files manually.

