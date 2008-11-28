#include <stdio.h>

extern const char g_compile_data[];

#ifndef WINCE 
# define _tmain main
#else
# include <tchar.h>
#endif
int _tmain()
{
	printf("Program compile data: %s\n", g_compile_data);

	return 0;
}
