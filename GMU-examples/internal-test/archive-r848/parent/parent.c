#include <stdio.h>

extern void child(void);

int main()
{
	child();
	return 0;
}
