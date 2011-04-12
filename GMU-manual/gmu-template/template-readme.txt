Here, we present two sets of template makefiles,
* one set is called concise     (directory name ends in -concise)
* another set is called verbose (directory name ends in -verbose)

The concise ones are new are recommended.

=============================================================================
After copying a -concise- template to your real project, you need to one thing:
=============================================================================

  Find all angle brackets enclosed in all Makefiles, modify them to
  your actual value. For example, in exe.mki , there is

		gmu_PRJ_NAME = <your-project-name>

  replace <your-project-name> with your real project name. If you forget to
  do this, the angle brackets in makefile will result in very strange behavior.


=============================================================================
After copying a -verbose- template to your real project, you need to modify 
two things:
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

2. Find all angle brackets enclosed content in all .mki files, modify them to
  your actual value. For example, in exe.mki , there is

		gmu_PRJ_NAME = <your-project-name>

  replace <your-project-name> with your real project name. If you forget to
  do this, the angle brackets in makefile will result in very strange behavior.


