#include <ctype.h>
#include "../ps_func.h"

/* Note: we do not consider MBCS file names(e.g. filename encoded in GBK 
 Chinese characters) here. -- We make it simple just for demonstration purpose.
*/
int walkdir_IsFileCharSame(int c1, int c2)
{
	if(toupper(c1) == toupper(c2))
		return 1; // true
	else
		return 0; // false
}
