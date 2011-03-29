#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>

#define DIRWALK_USER_CONST
#include <walkdir.h>


char * 
TrSearchString(const char *pInAbsdir, int *pRegularLen)
{
	char *pszNewSearchString = NULL;
	
	int inlen = strlen(pInAbsdir);
	if(pInAbsdir[inlen-1]=='/')
		inlen--;

	pszNewSearchString = (char*)malloc(inlen+1);
	assert(pszNewSearchString);

	strcpy(pszNewSearchString, pInAbsdir);

	*pRegularLen = inlen;
	return pszNewSearchString;
}

int IsDotAndDotDot(const char *pName)
{
	if(pName[0]=='.')
	{
		if(pName[1]=='\0')
			return 1;
		else if(pName[1]=='.' && pName[2]=='\0')
			return 1;
	}
	return 0;
}

walkdir_RET_et 
WalkDir_OneLevel(int DirLevelNow, 
	walkdir_CBINFO_st *pCbinfo, 
	PROC_WALKDIR_CALLBACK procWalkDirGotOne, void *pCallbackExtra)
{
	/*
		Input: pCbinfo->pszDir, pCbinfo->nDirLen
	*/

	walkdir_RET_et walkret = walkdir_RET_Success; // init not necessary
	walkdir_CBRET_et cbret = walkdir_CBRET_GoOn; // init not necessary
	
	DIR             *dp;
	struct dirent   *direntp;
	
	if(DirLevelNow>0)
	{
		pCbinfo->CallbackReason = walkdir_CBReason_EnterDir;
		pCbinfo->nDirLen = strlen(pCbinfo->pszDir);
		pCbinfo->nFileBytes = 0;
		pCbinfo->nDirLevel = DirLevelNow;
		// NOTE: pCbinfo->timeModified should have been filled by parent level(for efficiency),
		// when on parent level's walkdir_CBReason_MeetDir callback.

		cbret = procWalkDirGotOne(pCbinfo, pCallbackExtra);
		if(cbret==walkdir_CBRET_Halt)
			return walkdir_RET_Canceled;
	}

	if ((dp = opendir(pCbinfo->pszDir)) == NULL)
	{
		if(DirLevelNow==0)
			return walkdir_RET_Fail;

		// Tell the user through callback that this dir fails 
		pCbinfo->CallbackReason = walkdir_CBReason_DirEnterFail;
		pCbinfo->nDirLevel = DirLevelNow;

		cbret = procWalkDirGotOne(pCbinfo, pCallbackExtra);
		if(cbret==walkdir_CBRET_Halt)
			return walkdir_RET_Canceled;
		else
			return walkdir_RET_Success; // Yes, we neglect this failure if user does not mind it.
		return 1;
	}

	for(; (direntp = readdir(dp)) != NULL; )
	{
		struct stat statinfo;
		

		if(IsDotAndDotDot(direntp->d_name))
			continue;

		// Check whether we got a directory

		// but construct a full path name first
		pCbinfo->pszName = direntp->d_name;
		pCbinfo->nNameLen = strlen(pCbinfo->pszName);
		pCbinfo->nPathLen = pCbinfo->nDirLen+1+pCbinfo->nNameLen;
		pCbinfo->pszPath = (char*)realloc(pCbinfo->pszPath, pCbinfo->nPathLen+1);
		assert(pCbinfo->pszPath);
		strcpy(pCbinfo->pszPath, pCbinfo->pszDir);
		pCbinfo->pszPath[pCbinfo->nDirLen] = '/';
		strcpy(pCbinfo->pszPath + pCbinfo->nDirLen+1, pCbinfo->pszName);

		if(stat(pCbinfo->pszPath, &statinfo)!=0)
		{
			// stat failed, ignore it, may be it has just been deleted.
			continue;
		}

		// Prepare the walkdir_CBINFO struct for callback

		pCbinfo->CallbackReason = S_ISDIR(statinfo.st_mode) ?
			walkdir_CBReason_MeetDir : walkdir_CBReason_MeetFile;

		pCbinfo->nFileBytes = (__int64)statinfo.st_size;
		
		pCbinfo->timeModified = statinfo.st_mtime;

		pCbinfo->nDirLevel = DirLevelNow;

		// Call user's callback

		cbret = procWalkDirGotOne(pCbinfo, pCallbackExtra);
		if(cbret==walkdir_CBRET_Halt)
		{
			walkret = walkdir_RET_Canceled;
			break;
		}	

		// Recurse the dirwalk if it is a dir and not walkdir_BypassDir

		if(pCbinfo->CallbackReason==walkdir_CBReason_MeetDir
			&& cbret!=walkdir_CBRET_BypassDir)
		{
			int origDirLen = pCbinfo->nDirLen; // to restore later
			
			pCbinfo->nDirLen += 1 + pCbinfo->nNameLen;
			
			pCbinfo->pszDir = (char*)realloc(pCbinfo->pszDir, pCbinfo->nDirLen+1);
			assert(pCbinfo->pszDir);
			pCbinfo->pszDir[origDirLen] = '/';
			strcpy(pCbinfo->pszDir+origDirLen+1, pCbinfo->pszName);

			walkret = WalkDir_OneLevel(DirLevelNow+1, pCbinfo, 
				procWalkDirGotOne, pCallbackExtra);

			if(walkret==walkdir_RET_Canceled)
				break;
			
			assert(walkret==walkdir_RET_Success);

			// Restore pCbinfo->pszDir and pCbinfo->nDirLen for current dir level.
			pCbinfo->nDirLen = origDirLen;
			pCbinfo->pszDir[origDirLen] = '\0';
		}

	}
	
	closedir(dp);

	// Call user's callback again(this time with walkdir_CBReason_LeaveDir)
	// We do this after the dir is closed, so that user can even delete the dir
	// in the following callback.
	if(DirLevelNow>0)
	{
		pCbinfo->nDirLevel = DirLevelNow;
		pCbinfo->CallbackReason = walkdir_CBReason_LeaveDir;
		cbret = procWalkDirGotOne(pCbinfo, pCallbackExtra);
		if(cbret==walkdir_CBRET_Halt)
			return walkdir_RET_Canceled;
		else
			return walkdir_RET_Success;
	}
	else
	{
		return walkret;
	}
}

walkdir_RET_et  
walkdir_go(const char *pAbsDir, PROC_WALKDIR_CALLBACK procWalkDirGotOne, void *pCallbackExtra)
{
	walkdir_RET_et walkret;
	walkdir_CBINFO_st cbinfo = {sizeof(walkdir_CBINFO_st)};

	cbinfo.pszDir = TrSearchString(pAbsDir, &cbinfo.nDirLen);
//	cbinfo.nDirLen = strlen(cbinfo.pszDir); // This will be set by WalkDir_OneLevel

	walkret = WalkDir_OneLevel(0, &cbinfo, procWalkDirGotOne, pCallbackExtra);

	free(cbinfo.pszPath);
	free(cbinfo.pszDir);
	return 0;
}

