
=============================================================================
After copying a template to your real project, you need to modify two things:
=============================================================================

1. Rename the "[compiler-id]" extension name to a real compiler ID supported
  by your GnumakeUniproc environment. For example, 

  rename
		exe.[compiler-id]
  to
		exe.msvc
  or to
		exe.linuxgcc
  etc.

2. Find all angle bracket enclosed content in all .mki files, modify them to
  your actuall value. For example, in exe.mki , there is

		gmu_PRJ_NAME = <your-project-name>

  replace <your-project-name> with your real project name. If you forget to
  do this, the angle brackets in makefile will result in very strange behavior.


