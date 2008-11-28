#include <stdio.h>
#include <stdlib.h>

/*
	argv[1]: file path for the input file
	Remaining arg[n]: Each arg[n] string can contain one or several characters. 
 This program counts the appearance of any chars appear in arg[n] in the input file, 
 and write each count to stdout.
	If no argc=2, then count all chars in the file.

	Example:
		fmkCountChar _CountCompile.cnt x cb a
	may output:
		3 1 0
	This means there are 3 x, 1 [c or b] and 0 a in the file _CountCompile.cnt .

*/

static int g_count[256];

int main(int argc, char *argv[])
{
	int i;
	int count = 0;
	FILE *fp;

	if(argc==1)
		return 1;

	fp = fopen(argv[1], "rb");
	if(!fp)
		return 1;

	for(;;)
	{
		unsigned char c;
		if( fread(&c, 1, 1, fp) == 1)
			g_count[c]++;
		else
			break;
	}

	fclose(fp);

	if(argc==2)
	{
		count = 0;
		for(i=0; i<256; i++)
			count += g_count[i];

		printf("%d", count);
	}
	else
	{
		for(i=2; i<argc; i++)
		{
			const char *pc = argv[i];
			count = 0;
			for(; *pc; pc++)
				count += g_count[*pc];

			printf("%d%s", count, i<argc-1 ? " " : "");
		}
	}

	printf("\n");
	return 0;
}
