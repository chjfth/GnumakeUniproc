#include <stdio.h>
#include "libtest1.h"
#include "libtest2.h"

void libtest1a()
{
	printf("libtest1a()\n");
}

void libtest1b()
{
	printf("libtest1b()\n");
	libtest2();
}

