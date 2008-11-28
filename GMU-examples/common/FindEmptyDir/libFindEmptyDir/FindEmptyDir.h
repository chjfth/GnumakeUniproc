#ifndef __FindEmptyDir_h_
#define __FindEmptyDir_h_

#ifdef __cplusplus
extern"C"{
#endif

typedef enum _FindEmptyDir_CBRET_et
{
	FindEmptyDir_CBRET_GoOn = 0,
	FindEmptyDir_CBRET_Halt = 2
}FindEmptyDir_CBRET_et;

typedef FindEmptyDir_CBRET_et (*PROC_FindEmptyDir_CALLBACK)(
	const char *pszEmptyDir, void *pCallbackExtra);


typedef enum _FindEmptyDir_RET_et
{
	FindEmptyDir_RET_Success = 0,
	FindEmptyDir_RET_Fail = -1,
	FindEmptyDir_RET_Canceled = -2
}FindEmptyDir_RET_et;

FindEmptyDir_RET_et FindEmptyDir(
	const char *pAbsDir, 
	PROC_FindEmptyDir_CALLBACK procFoundEmptyDir, 
	void *pCallbackExtra);


#ifdef __cplusplus
} // extern"C"{
#endif

#endif
