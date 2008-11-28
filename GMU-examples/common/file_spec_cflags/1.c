#include <stdio.h>
#include "w.h"

int ReturnNumA()
{
	return INPUT_NUM;
}

int main()
{
	printf("ReturnNumA()=%d\n", ReturnNumA());
	printf("ReturnNumB()=%d\n", ReturnNumB());
	return 0;
}
