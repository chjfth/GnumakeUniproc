#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
	argv[1]: file path for the input file
	argv[2]: the word to append to file(append only if not existed in file yet)
*/

#define PREFIX "gmuAddActionWord: "

#define FILEBUFSIZE 32000
static char g_szFileBuf[FILEBUFSIZE+1];

int GetFileSize(FILE *fp)
{
	fseek(fp, 0, SEEK_END);
	return ftell(fp);
}

void ReadFileContent(FILE *fp)
{
	int nRd = 0;

	fseek(fp, 0, SEEK_SET);
	nRd = fread(g_szFileBuf, 1, FILEBUFSIZE, fp);
	if(nRd<0)
	{
		fprintf(stderr, PREFIX"Error reading file content.\n");
		exit(1);
	}

	g_szFileBuf[FILEBUFSIZE] = '\0';
}

int main(int argc, char *argv[])
{
	const char *szfn = NULL;
	FILE *fp = NULL;
	int flen = 0;
	int lenStem = 0;
	char *pszStem = NULL;

	if(argc<3)
	{
		fprintf(stderr, PREFIX"Error. Missing parameters: arg1=filepath arg2=word.\n");
		return 1;
	}

	szfn = argv[1];
	
	fp = fopen(szfn, "rb+");
	if(!fp)
	{
		fprintf(stderr, PREFIX"Error opening %s for read-write.\n", szfn);
		return 1;
	}

	flen  = GetFileSize(fp);
	if(flen>FILEBUFSIZE)
	{
		fprintf(stderr, PREFIX"Error. File size exceeds %d.\n", FILEBUFSIZE);
		return 1;
	}

	ReadFileContent(fp);

	lenStem = strlen(argv[2])+2;
	pszStem = (char*)malloc(lenStem+1);
	assert(pszStem);

	sprintf(pszStem, "\n%s\n", argv[2]);

	if(strstr(g_szFileBuf, pszStem)==NULL)
	{
		int nWr = fwrite(pszStem, 1, lenStem, fp);
		if(nWr!=lenStem)
		{
			fprintf(stderr, PREFIX"Error writing file, will write %d but return %d.\n", 
				lenStem, nWr);
			return 1;
		}
	}

	return 0;
}
