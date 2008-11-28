#include <stdio.h>

#define DEFINE_CALL(funcname, callinto) \
	void funcname() { \
		printf(__FILE__ "\t" #funcname "() -> " #callinto "()\n"); \
		callinto(); \
	}

/* Example:

DEFINE_CALL(a1, b1)

// becomes:

void a1() { 
	printf(__FILE__ "\t" "a1() -> b1()\n"); 
	b1(); 
}

*/
