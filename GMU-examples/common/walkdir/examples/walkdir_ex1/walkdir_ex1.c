#include <stdio.h>
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

	if(pCbinfo->CallbackReason==walkdir_CBReason_MeetDir
		||pCbinfo->CallbackReason==walkdir_CBReason_MeetFile) // meet a dir or file
	{
		ptm = localtime(&pCbinfo->timeModified);

		PrintChars(pCbinfo->nDirLevel, ' ');
		printf("%s (%d)\n", pCbinfo->pszPath, pCbinfo->nPathLen);
		PrintChars(pCbinfo->nDirLevel, ' ');
		printf("%s/%s (%d)\n", pCbinfo->pszDir, pCbinfo->pszName, pCbinfo->nDirLen+pCbinfo->nNameLen+1);
		PrintChars(pCbinfo->nDirLevel, ' ');
		printf("[level %d] %d-%02d-%02d %02d:%02d:%02d (%s)\n", pCbinfo->nDirLevel,
			ptm->tm_year+1900, ptm->tm_mon+1, ptm->tm_mday,
			ptm->tm_hour, ptm->tm_min, ptm->tm_sec,
			pCbinfo->CallbackReason==walkdir_CBReason_MeetDir?"CBReason_MeetDir":"CBReason_MeetFile");
		printf("\n");

		(*pTotal)++;
	}
	else if(pCbinfo->CallbackReason==walkdir_CBReason_EnterDir) 		// walkdir_CBReason_LeaveDir
	{
		PrintChars(pCbinfo->nDirLevel, '>');
		printf("[level %d] %s (CBReason_EnterDir) (%d)\n\n", pCbinfo->nDirLevel, pCbinfo->pszDir, pCbinfo->nDirLen);
	}
	else if(pCbinfo->CallbackReason==walkdir_CBReason_LeaveDir) 		// walkdir_CBReason_LeaveDir
	{
		PrintChars(pCbinfo->nDirLevel, '<');
		printf("[level %d] %s (CBReason_LeaveDir) (%d)\n\n", pCbinfo->nDirLevel, pCbinfo->pszDir, pCbinfo->nDirLen);
	}
	else if(pCbinfo->CallbackReason==walkdir_CBReason_DirEnterFail)
	{
		fprintf(stderr, "[Level %d]Cannot enter: %s\n\n", pCbinfo->nDirLevel, pCbinfo->pszDir);
		return walkdir_CBRET_GoOn;
	}

	return walkdir_CBRET_GoOn;
}


//Usage:
//1: exe_name path
//2: exe_name path exttype
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
		walkret = walkdir_go(pAbsDir, pcbWalkdir, (void*)&nTotal);
	}
	else
	{
		walkret = walkdir_extname(pAbsDir, argv+2, argc-2, pcbWalkdir, (void*)&nTotal);
	}

	if(walkret==walkdir_RET_Fail)
	{
		printf("walkdir_RET_Fail\n");
	}
	else
	{
		printf("walkdir_RET_Success, nTotal = %d\n", nTotal);
	}

	return 0;
}

/*
	[2007-01-05 22:11] Strange!
	On SuSE Linux 10.1 32-bit, running this program with starting dir "/dev/fd"
 will lead to infinite loop. Simple debug with kdbg shows that 
 /dev/fd/0 , /dev/fd/1 , ... are enumerated, but when /dev/fd/8 is met, 
 its stat.st_mode is 040500(octal), which causes S_ISDIR() return true for it. 
 This occurs again and again for /dev/fd/8/8 , /dev/fd/8/8/8 ... 
*/
