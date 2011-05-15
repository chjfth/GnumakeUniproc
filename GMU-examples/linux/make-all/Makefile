# template file for use with pattern1-container.mks, concise version, [GnumakeUniproc v1.0]
# ! Be sure to replace every occurrence of <angle-brackets> to be your
# actual content, or [ at least comment them out if some of them are
# not required] .
ifdef gmu_DIR_GNUMAKEUNIPROC
  include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-concise-header.mki
else
  $(error gmu_DIR_GNUMAKEUNIPROC is not defined, You have to set up GnumakeUniproc environment to use this Makefile)
endif

ifndef gmu_PRJ_NAME
  gmu_PRJ_NAME = GMU-examples-linux-all
endif

gmu_uv_list_ALL_SUBPRJ += gtktetris-pch gtktetris-strip

gtktetris-pch_Makefile = ../gtk-tetris/gtktetris-gmu/make-PI_use_pch_gcc/Makefile

gtktetris-strip_Makefile = ../gtk-tetris/gtktetris-gmu/make-PI_gcc_strip_lo/Makefile


include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-container.mks

