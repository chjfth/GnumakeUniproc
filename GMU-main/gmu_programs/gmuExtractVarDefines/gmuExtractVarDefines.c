#include <stdio.h>
#include <string.h>

/*
	Used to extract only the variable definition part from $(MAKEFLAGS).
 If some var-def is given as make's command line, make will separate 
 make options and var-defs with -- , so, I'll throw off anything before -- .
 
	Example:
	1.
		make --debug=m
$(MAKEFLAGS)=
		--debug=m

	2.
		make bc_DEBUG=1
$(MAKEFLAGS)=
		bc_DEBUG=1

	3.
		make -w --debug=m bc_DEBUG=1
$(MAKEFLAGS)=
		w --debug=m -- bc_DEBUG=1

	4.
		make -w bc_DEBUG=1
$(MAKEFLAGS)=
		w -- bc_DEBUG=1

	5.
		make -w
$(MAKEFLAGS)=
		w

	6.
		make --debug=m
$(MAKEFLAGS)=
		 --debug=m			(Look, there is a preceding space.)

*/

#define PREFIX "gmuExtractVarDefines: "

int main(int argc, char *argv[])
{
	const char *pszAllStr = NULL;
	const char *pszSign = NULL;
	int lenSign = 0;
	const char *pszFound = NULL;

	if(argc==1)
	{
		fprintf(stderr, PREFIX"No input string as argument.");
		return 1;
	}

	pszAllStr = argv[1];
	pszSign = " -- ";
	lenSign = strlen(pszSign);
	pszFound = strstr(pszAllStr, pszSign);
	
	if(pszFound)
	{
		printf("%s", pszFound+lenSign);
	}
	else if(strstr(pszAllStr, " --")==NULL && strchr(pszAllStr, '=')!=NULL);
	{
		printf("%s", pszAllStr);
	}

	return 0;
}
