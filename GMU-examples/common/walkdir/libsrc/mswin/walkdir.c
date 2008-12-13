#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <windows.h>

#define DIRWALK_USER_CONST
#include <walkdir.h>


#define FINDSTR_OVERHEAD 2
	// 2 is for "/*" append to a dir

char * 
TrSearchString(const char *pInAbsdir, int *pRegularLen)
{
	char *pszNewSearchString = NULL;
	
	int inlen = strlen(pInAbsdir);
	if(pInAbsdir[inlen-1]=='/')
		inlen--;

	pszNewSearchString = (char*)malloc(inlen+FINDSTR_OVERHEAD+1);
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

time_t 
FiletimeToANSICTime(FILETIME *pFiletime)
{
	SYSTEMTIME st;
	struct tm tmAnsi;

	FileTimeToSystemTime(pFiletime, &st);	
	tmAnsi.tm_year = st.wYear-1900;	
	tmAnsi.tm_mon = st.wMonth-1;
	tmAnsi.tm_mday = st.wDay;
	tmAnsi.tm_hour = st.wHour;
	tmAnsi.tm_min = st.wMinute;
	tmAnsi.tm_sec = st.wSecond;
	tmAnsi.tm_isdst = 0; // not daylight saving time
	tmAnsi.tm_wday = tmAnsi.tm_yday = 0; // Seems these two can be arbitrary for mktime.

	return mktime(&tmAnsi);
}

walkdir_RET_et 
WalkDir_OneLevel(int DirLevelNow, 
	walkdir_CBINFO_st *pCbinfo, 
	PROC_WALKDIR_CALLBACK procWalkDirGotOne, void *pCallbackExtra)
{
	/*
		Input: pCbinfo->pszDir, pCbinfo->nDirLen
	*/

	BOOL b = 0; DWORD winerr = 0;
	WIN32_FIND_DATA finddata;
	HANDLE hff = NULL; // find-handle
	FILETIME ftLocal;
	walkdir_RET_et walkret = walkdir_RET_Success; // init not necessary
	walkdir_CBRET_et cbret = walkdir_CBRET_GoOn; // init not necessary

	// Prepare the "search string format" required for FindFirstFile.
	// You know we have allocated FINDSTR_OVERHEAD(2) more bytes for pCbinfo->pszDir
	pCbinfo->pszDir[pCbinfo->nDirLen] = '/';
	pCbinfo->pszDir[pCbinfo->nDirLen+1] = '*';
	pCbinfo->pszDir[pCbinfo->nDirLen+2] = '\0';
	
	hff = FindFirstFile(pCbinfo->pszDir, &finddata);

	pCbinfo->pszDir[pCbinfo->nDirLen] = '\0';
		// Remove the "/*" suffix here since it's no longer necessary.

	if(hff==INVALID_HANDLE_VALUE)
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
	}

	for(;;)
	{
		if(IsDotAndDotDot(finddata.cFileName))
			goto FIND_NEXT_FILE;

		// Prepare the walkdir_CBINFO struct for callback

		pCbinfo->nDirLevel = DirLevelNow;
	
		pCbinfo->CallbackReason = 
			(finddata.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY) ?
			walkdir_CBReason_EnterDir : walkdir_CBReason_MeetFile;
		pCbinfo->pszName = finddata.cFileName;
		pCbinfo->nNameLen = strlen(pCbinfo->pszName);
		pCbinfo->nPathLen = pCbinfo->nDirLen+1+pCbinfo->nNameLen;
		pCbinfo->pszPath = (char*)realloc(pCbinfo->pszPath, pCbinfo->nPathLen+1);
		assert(pCbinfo->pszPath);
		strcpy(pCbinfo->pszPath, pCbinfo->pszDir);
		pCbinfo->pszPath[pCbinfo->nDirLen] = '/';
		strcpy(pCbinfo->pszPath + pCbinfo->nDirLen+1, pCbinfo->pszName);

		pCbinfo->nFileBytes = ((__int64)finddata.nFileSizeHigh<<32) | finddata.nFileSizeLow;
		
		FileTimeToLocalFileTime(&finddata.ftLastWriteTime, &ftLocal);
		pCbinfo->timeModified = FiletimeToANSICTime(&ftLocal);

		// Call user's callback

		cbret = procWalkDirGotOne(pCbinfo, pCallbackExtra);
		if(cbret==walkdir_CBRET_Halt)
		{
			walkret = walkdir_RET_Canceled;
			break;
		}	

		// Recurse the dirwalk if it is a dir and not walkdir_BypassDir

		if(pCbinfo->CallbackReason==walkdir_CBReason_EnterDir
			&& cbret!=walkdir_CBRET_BypassDir)
		{
			int origDirLen = pCbinfo->nDirLen; // to restore later
			
			pCbinfo->nDirLen += 1 + pCbinfo->nNameLen;
			
			pCbinfo->pszDir = (char*)realloc(pCbinfo->pszDir, pCbinfo->nDirLen+FINDSTR_OVERHEAD+1);
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

FIND_NEXT_FILE:

		b = FindNextFile(hff, &finddata);
		if(b)
			continue;
		else
		{
			winerr = GetLastError();
			if(winerr==ERROR_MORE_DATA) // ERROR_MORE_DATA=234
			{
				// Note: If you use ANSI version of FindNextFile and a file is encountered
				// with MAX_PATH-1 characters, then the ANSI length of the file can 
				// exceed MAX_PATH bytes, so ERROR_MORE_DATA will be returned.
				// For simplicity here, we just ignore it.
				continue;
			}

			assert(winerr==ERROR_NO_MORE_FILES); // ERROR_NO_MORE_FILES=18
			walkret = walkdir_RET_Success;
			break;
		}
	}
	
	FindClose(hff);

	// Call user's callback again(this time with walkdir_CBReason_LeaveDir)
	// We do this after the dir is closed, so that user can even delete the dir
	//in the following callback.
	if(cbret!=walkdir_CBRET_Halt)
	{
		pCbinfo->nDirLevel = DirLevelNow;
		pCbinfo->CallbackReason = walkdir_CBReason_LeaveDir;
		cbret = procWalkDirGotOne(pCbinfo, pCallbackExtra);
		if(cbret==walkdir_CBRET_Halt)
			walkret = walkdir_RET_Canceled;
	}

	return walkret;
}

walkdir_RET_et  
walkdir_start(const char *pAbsDir, PROC_WALKDIR_CALLBACK procWalkDirGotOne, void *pCallbackExtra)
{
	walkdir_RET_et walkret;
	walkdir_CBINFO_st cbinfo = {sizeof(walkdir_CBINFO_st)};

	//char *pszSearchString //
	cbinfo.pszDir = TrSearchString(pAbsDir, &cbinfo.nDirLen);

	walkret = WalkDir_OneLevel(0, &cbinfo, procWalkDirGotOne, pCallbackExtra);

	free(cbinfo.pszPath);
	free(cbinfo.pszDir);
	return 0;
}

