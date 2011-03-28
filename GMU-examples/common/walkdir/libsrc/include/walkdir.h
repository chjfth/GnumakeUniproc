#ifndef __walkdir_h_20070102_
#define __walkdir_h_20070102_

#ifdef __cplusplus
extern"C"{
#endif

//#include <stdio.h>
#include <time.h>


#ifndef DIRWALK_USER_CONST 
# define DIRWALK_USER_CONST const
#endif

typedef enum _walkdir_CBRET_et
{
	walkdir_CBRET_GoOn = 0,
	walkdir_CBRET_BypassDir = 1,
	walkdir_CBRET_Halt = 2
}walkdir_CBRET_et;


typedef enum _walkdir_CBReason_et
{
	walkdir_CBReason_MeetFile = 1,
	walkdir_CBReason_MeetDir  = 2,
	walkdir_CBReason_EnterDir = 3,
	walkdir_CBReason_LeaveDir = 4,
	walkdir_CBReason_DirEnterFail = 5,
}walkdir_CBReason_et;

typedef struct _walkdir_CBINFO_st
{
	int StructSize;

	walkdir_CBReason_et CallbackReason;

	DIRWALK_USER_CONST char *pszPath;
	int nPathLen;
	DIRWALK_USER_CONST char *pszDir;
	int nDirLen;
	DIRWALK_USER_CONST char *pszName;
	int nNameLen;

	__int64 nFileBytes;

	time_t timeModified;

	int nDirLevel;
}walkdir_CBINFO_st;


typedef walkdir_CBRET_et (*PROC_WALKDIR_CALLBACK)(
	const walkdir_CBINFO_st *pCbinfo, void *pCallbackExtra
	);


typedef enum _walkdir_RET_et
{
	walkdir_RET_Success = 0,
	walkdir_RET_Fail = -1,
	walkdir_RET_Canceled = -2
}walkdir_RET_et;

walkdir_RET_et walkdir_go(
	const char *pAbsDir, 
	PROC_WALKDIR_CALLBACK procWalkDirGotOne, 
	void *pCallbackExtra);

walkdir_RET_et walkdir_extname(
	const char *pAbsDir, 
	const char * const arpExtName[], int nExtName, 
	PROC_WALKDIR_CALLBACK procWalkDirGotOne, 
	void *pCallbackExtra);

#ifdef __cplusplus
} //extern"C"{
#endif

#endif

