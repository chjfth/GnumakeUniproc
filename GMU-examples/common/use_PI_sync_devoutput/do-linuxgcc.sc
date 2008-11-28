# This file should be run in bash shell using source command from this very dir.
# e.g.
# source do-linuxgcc.sc
cd ../walkdir/libsrc/makelib/lib.linuxgcc
umake gmu_DO_SHOW_VERBOSE=2 gmp_u_list_PLUGIN_TO_LOAD=PI_sync_devoutput gmi_SYDO_ud_SYNC_HEADER_TO=$gmu_DIR_ROOT/mysdk/include gmi_SYDO_ud_SYNC_LIB_TO=$gmu_DIR_ROOT/mysdk/lib
cd -
