#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <walkdir.h>
#include "ps_func.h"

int 
IsOneExtMatch(const char *pName, const char *pExtName)
{
	// Note, for a name like ".ssh" , we consider it not having a ext-name. 
	// For ".ssh.txt", it has the ext-name "txt".

	const char *pDot = NULL;
	
	// Find the last dot in the filename(pName).
	pDot = strrchr(pName, '.');
	if(!pDot || pDot==pName) 
	{
		// `pName' has not ext-name 
		return pExtName[0] ? 0 : 1; // 0=No, 1=Yes
	}

	// Compare the part after dot

	pDot++;
	for(;;pDot++,pExtName++)
	{
		if(!walkdir_IsFileCharSame(*pDot, *pExtName))
			return 0; // No

		if(*pDot=='\0')
			return 1;
	}
}

typedef struct _SWalkdirExtname
{
	const char * const*arpExtName;
	int nExtName;
	PROC_WALKDIR_CALLBACK user_proc; // Store user's procWalkDirGotOne
	void *user_cbextra;		// Store user's pCallbackExtra
}SWalkdirExtname;

walkdir_CBRET_et
procWalkdirExtname(const walkdir_CBINFO_st *pCbinfo, void *pCallbackExtra)
{
	int i;
	SWalkdirExtname *pwei = (SWalkdirExtname*)pCallbackExtra;
	const char * const *arpExtName = pwei->arpExtName;
	int nExtName = pwei->nExtName;

	// If we got a dir-enter failure notification, notify it to our user.

	if(pCbinfo->CallbackReason==walkdir_CBReason_DirEnterFail)
	{
		return pwei->user_proc(pCbinfo, pwei->user_cbextra);
	}

	// If we got a dir entry, ignore it for our user.

	if(pCbinfo->CallbackReason==walkdir_CBReason_EnterDir)
		return walkdir_CBRET_GoOn;

	// Now, we check whether we got a file with user-specified extension.

	for(i=0; i<nExtName; i++)
	{
		if(IsOneExtMatch(pCbinfo->pszName, arpExtName[i]))
		{
			return pwei->user_proc(pCbinfo, pwei->user_cbextra);
		}
	}

	return walkdir_CBRET_GoOn;
}

walkdir_RET_et walkdir_extname(
	const char *pAbsDir, 
	const char * const arpExtName[], int nExtName, 
	PROC_WALKDIR_CALLBACK procWalkDirGotOne, 
	void *pCallbackExtra)
{
	walkdir_RET_et walkret;
	SWalkdirExtname wei = {0}, *pwei = &wei; // wei: walkdir extname info
	pwei->arpExtName = arpExtName;
	pwei->nExtName = nExtName;
	pwei->user_proc = procWalkDirGotOne;
	pwei->user_cbextra = pCallbackExtra;

	walkret = walkdir_go(pAbsDir, procWalkdirExtname,pwei);

	return walkret;
}


