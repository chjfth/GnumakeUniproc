# template file for use with pattern1-container.mks, concise version, [GnumakeUniproc v1.0]
# ! Be sure to replace every occurrence of <angle-brackets> to be your
# actual content, or [ at least comment them out if some of them are
# not required] .
ifdef gmu_DIR_GNUMAKEUNIPROC
  include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-concise-header.mki

  include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1cfg/compiler-env/cenv-msvc-vc60.mki
	# To get function gmpf_LoadCenv_msvc_vc60
  include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1cfg/compiler-env/cenv-msvc-vc80.mki
	# To get function gmpf_LoadCenv_msvc_vc80

  #Note: If you are using other MSVC version, add corresponding mki please.
else
  $(error gmu_DIR_GNUMAKEUNIPROC is not defined, You have to set up GnumakeUniproc environment to use this Makefile)
endif

ifndef gmu_PRJ_NAME
  gmu_PRJ_NAME = walkdir-msvc-multiver
endif

export gmp_COMPILER_ID=msvc
	# We see it so that user don't have to set it in env forehand.

gmu_uv_list_ALL_SUBPRJ += walkdir_vc60 walkdir_vc80

shared_makefile = ../../common/walkdir/make-all/all.$(gmp_COMPILER_ID)/Makefile

walkdir-vc60_Makefile = $(shared_makefile)
walkdir-vc60_MakeVarDefines = $(gmpf_LoadCenv_msvc_vc60)

walkdir-vc80_Makefile = $(shared_makefile)
walkdir-vc80_MakeVarDefines = $(gmpf_LoadCenv_msvc_vc80)


include $(gmu_DIR_GNUMAKEUNIPROC)/pattern1-container.mks

