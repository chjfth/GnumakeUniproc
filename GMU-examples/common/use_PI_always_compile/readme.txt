This project demonstrates how to use a plugin. The plugin used in this example
is PI_always_compile.

This project consists of two C source files: main.c and nowdate.c , and 
we'd like nowdate.c to be always compiled, that is, when make is run, date.c
always get re-compiled into nowdate.obj,-- even if nowdate.obj is newer than
nowdate.c . This is useful when you use C internal macro __DATE__ or __TIME__
to represent a program's build date. 
In order to do this, we need extra two steps:

1. Load the plugin PI_always_compile in makefile:
=======
gmp_u_list_PLUGIN_TO_LOAD += PI_always_compile
=======

2. Tell which files should be always compiled:
=======
gmi_ALCP_up_list_SRC_ALWAYS_COMPILE_FROM_ROOT = nowdate.c
=======

That's it.
