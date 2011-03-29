#include <walkdir.h>

#include "FindEmptyDir.h"

struct SFindEmptyDirCbinfo // Cbinfo: callback info
{
	PROC_FindEmptyDir_CALLBACK cbFoundEmptyDir;
	void *pcbeFindEmptyDir; // FindEmptyDir's user callback extra void*

	int EmptyFlag;

	enum // Used by PrevEmptyFlag
	{
		ThisDirNotEmpty = 0,
		ThisDirEmpty = 1
	};
};


walkdir_CBRET_et 
WalkdirCallback_Fed(const walkdir_CBINFO_st *pWalkdirCbi, void *pCallbackExtra)
{
	SFindEmptyDirCbinfo *pFedCbi = (SFindEmptyDirCbinfo*)pCallbackExtra;

	if(pWalkdirCbi->CallbackReason==walkdir_CBReason_EnterDir)
	{
		pFedCbi->EmptyFlag = SFindEmptyDirCbinfo::ThisDirEmpty;
			// Assume the dir just entered is empty.
	}
	else if(pWalkdirCbi->CallbackReason==walkdir_CBReason_MeetFile)
	{
		pFedCbi->EmptyFlag = SFindEmptyDirCbinfo::ThisDirNotEmpty;
	}
	else if(pWalkdirCbi->CallbackReason==walkdir_CBReason_LeaveDir)
	{
		if(pFedCbi->EmptyFlag==SFindEmptyDirCbinfo::ThisDirEmpty)
		{	// Now an empty dir is confirmed.
			FindEmptyDir_CBRET_et fedret = 
				pFedCbi->cbFoundEmptyDir
				(
					pWalkdirCbi->pszPath, 
					pFedCbi->pcbeFindEmptyDir
				);
			
			if(fedret==FindEmptyDir_CBRET_Halt)
				return walkdir_CBRET_Halt;
		}

		pFedCbi->EmptyFlag = SFindEmptyDirCbinfo::ThisDirNotEmpty;
			// If we've leaving /dir1/dir2 (pCbinfo->pszPath now is /dir1/dir2),
			// we set this so that /dir1 's context will see ThisDirNotEmpty.
	}

	return walkdir_CBRET_GoOn;
}


FindEmptyDir_RET_et 
FindEmptyDir(
	const char *pAbsDir, 
	PROC_FindEmptyDir_CALLBACK procFoundEmptyDir, 
	void *pCallbackExtra)
{
	SFindEmptyDirCbinfo fedcbi = {0};
	fedcbi.cbFoundEmptyDir = procFoundEmptyDir;
	fedcbi.pcbeFindEmptyDir = pCallbackExtra;

	walkdir_RET_et walkret = walkdir_go(pAbsDir, WalkdirCallback_Fed, &fedcbi);
	
	if(walkret==walkdir_RET_Success)
		return FindEmptyDir_RET_Success;
	else if(walkret==walkdir_RET_Fail)
		return FindEmptyDir_RET_Fail;
	else // if(walkret==walkdir_RET_Canceled)
		return FindEmptyDir_RET_Canceled;
}

