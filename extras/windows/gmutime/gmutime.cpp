/* [2007-01-29]
	Use this program to measure the time one GnumakeUniproc run costs.
	
	With argument '0', this program creates a file named gmustart.msec in current dir containing
 the current millisecond time stamp. With argument 1, this program reads gmustart.msec's content
 and compare it to current millisecond time stamp to get a time delta then send it to stdout.
*/
#include <stdio.h>
#include <windows.h>

#define SZFN_START_TIME "gmustart.msec"

int main(int argc, char **argv)
{
	if(argc!=2)
		return 1;

	int nowtime = GetTickCount();

	FILE *fp = NULL;

	if(*argv[1] == '0') // create new time file
	{
		fp = fopen(SZFN_START_TIME, "wb+");
		if(!fp)
			return 2;

		fwrite(&nowtime, 1, sizeof(int), fp);
		
	}
	else // count time delta
	{
		int oldtime;
		fp = fopen(SZFN_START_TIME, "rb");
		if(!fp)
			return 2;

		fread(&oldtime, 1, sizeof(int), fp);
		
		int delta_msec = nowtime-oldtime;
		
		printf("Gmu seconds used: %d.%d", delta_msec/1000, delta_msec%1000);
	}
	
	fclose(fp);

	return 0;
}
