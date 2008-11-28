#include <stdio.h>

#ifdef __linux__
# include <unistd.h>
#else
# include <direct.h>

#endif

#include <walkdir.h>

static void 
PrintChars(int n, int c)
{
	while(--n>=0)
		printf("%c", c);
}

walkdir_CBRET_et pcbWalkdir(
	const walkdir_CBINFO_st *pCbinfo, void *pCallbackExtra
	)
{
	int *pTotal = (int*)pCallbackExtra;
	struct tm *ptm;

	if(pCbinfo->CallbackReason==walkdir_CBReason_DirEnterFail)
	{
		printf("[Level %d]Cannot enter: %s\n\n", pCbinfo->nDirLevel, pCbinfo->pszDir);
		return walkdir_CBRET_GoOn;
	}

	if(pCbinfo->CallbackReason==walkdir_CBReason_MeetFile) // meet a file
	{
		ptm = localtime(&pCbinfo->timeModified);

		PrintChars(pCbinfo->nDirLevel, ' ');
		printf("%s/%s (%d)\n", pCbinfo->pszDir, pCbinfo->pszName, pCbinfo->nDirLen+pCbinfo->nNameLen+1);
		int re = remove(pCbinfo->pszPath);
		if(re!=0)
			printf("!!!!!! remove() fail.");
		printf("\n");
	}
	else if(pCbinfo->CallbackReason==walkdir_CBReason_LeaveDir)
	{
		PrintChars(pCbinfo->nDirLevel, '<');
		printf("[level %d] %s (%d)\n", pCbinfo->nDirLevel, pCbinfo->pszDir, pCbinfo->nDirLen);
		int re = rmdir(pCbinfo->pszDir);
		if(re!=0)
			printf("!!!! rmdir() fail.");
		printf("\n");
	}

	(*pTotal)++;

	return walkdir_CBRET_GoOn;
}

int main(int argc, char *argv[])
{
	const char *pAbsDir = NULL;
	walkdir_RET_et walkret;
	int nTotal = 0;

	if(argc<2)
	{
		printf("Please input a dir as the param.\n");
		return 1;
	}

	pAbsDir = argv[1];
	
	if(argc==2)
	{
		walkret = walkdir_start(pAbsDir, pcbWalkdir, (void*)&nTotal);
	}

	if(walkret==walkdir_RET_Fail)
	{
		printf("walkdir_RET_Fail\n");
	}
	else
	{
		printf("walkdir_RET_Success, nTotal = %d\n\n", nTotal);
	}

	return 0;
}

