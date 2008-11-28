#include <stdio.h>

#include <FindEmptyDir.h>

FindEmptyDir_CBRET_et cbFoundEmptyDir(
	const char *pszEmptyDir, void *pCallbackExtra
	)
{
	int *pTotal = (int*)pCallbackExtra;
	(*pTotal)++;

	printf("[%d] %s\n", *pTotal, pszEmptyDir);

	return FindEmptyDir_CBRET_GoOn;
}

int main(int argc, char *argv[])
{
	const char *pAbsDir = NULL;
	FindEmptyDir_RET_et fedret;
	int nTotal = 0;

	if(argc<2)
	{
		printf("demoFindEmptyDir: Please input a dir as the param.\n");
		return 1;
	}

	pAbsDir = argv[1];

	fedret = FindEmptyDir(pAbsDir, cbFoundEmptyDir, (void*)&nTotal);

	if(fedret==FindEmptyDir_RET_Fail)
	{
		printf("FindEmptyDir_RET_Fail\n");
	}
	else
	{
		printf("FindEmptyDir_RET_Success. Total empty dirs = %d .\n", nTotal);
	}

	return 0;
}

