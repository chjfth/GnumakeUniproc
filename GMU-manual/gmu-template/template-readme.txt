
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

2. Find all angle bracket enclosed content in all .mki files, modify them to
  your actuall value. For example, in exe.mki , there is

		gmu_PRJ_NAME = <your-project-name>

  replace <your-project-name> with your real project name. If you forget to
  do this, the angle brackets in makefile will result in very strange behavior.


=============================================================================
NOTE for DLL projects:
=============================================================================

DLL project should use template "make-exe" instead of "make-lib", since DLL
may need to link other libs as EXE projects do. 

Remember, gmp_bc_IMAGE_TYPE should be modified to "DLL" .

By the way, when setting gmu_uf_LINK_OUTPUT, it is suggested to use function
gmpf_MakeDllNameForLink to construct its value.

Example:

		gmu_uf_LINK_OUTPUT = $(call gmpf_MakeDllNameForLink,ZLIB1)


