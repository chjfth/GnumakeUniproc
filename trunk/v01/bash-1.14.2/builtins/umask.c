/* umask.c, created from umask.def. */
#line 23 "./umask.def"

#line 33 "./umask.def"

#include <stdio.h>
#include <sys/types.h>
#include <sys/file.h>
#include "shell.h"
#include "posixstat.h"
#include "common.h"

/* **************************************************************** */
/*                                                                  */
/*                     UMASK Builtin and Helpers                    */
/*                                                                  */
/* **************************************************************** */

static void print_symbolic_umask ();
static int symbolic_umask ();

/* Set or display the mask used by the system when creating files.  Flag
   of -S means display the umask in a symbolic mode. */
umask_builtin (list)
     WORD_LIST *list;
{
  int print_symbolically = 0;

  while (list)
    {
      if (ISOPTION (list->word->word, 'S'))
	{
	  list = list->next;
	  print_symbolically++;
	  continue;
	}
      else if (ISOPTION (list->word->word, '-'))
	{
	  list = list->next;
	  break;
	}
      else if (*(list->word->word) == '-')
	{
	  bad_option (list->word->word);
	  builtin_error ("usage: umask [-S] [mode]");
	  return (EX_USAGE);
	}
      else
	break;
    }

  if (list)
    {
      int new_umask;

      if (digit (*list->word->word))
	{
	  new_umask = read_octal (list->word->word);

	  /* Note that other shells just let you set the umask to zero
	     by specifying a number out of range.  This is a problem
	     with those shells.  We don't change the umask if the input
	     is lousy. */
	  if (new_umask == -1)
	    {
	      builtin_error ("`%s' is not an octal number from 000 to 777",
				list->word->word);
	      return (EXECUTION_FAILURE);
	    }
	}
      else
	{
	  new_umask = symbolic_umask (list);
	  if (new_umask == -1)
	    return (EXECUTION_FAILURE);
	}
      umask (new_umask);
      if (print_symbolically)
	print_symbolic_umask (new_umask);
    }
  else				/* Display the UMASK for this user. */
    {
      int old_umask;

      old_umask = umask (022);
      umask (old_umask);

      if (print_symbolically)
	print_symbolic_umask (old_umask);
      else
	printf ("%03o\n", old_umask);
    }
  fflush (stdout);
  return (EXECUTION_SUCCESS);
}

/* Print the umask in a symbolic form.  In the output, a letter is
   printed if the corresponding bit is clear in the umask. */
static void
print_symbolic_umask (um)
     int um;
{
  char ubits[4], gbits[4], obits[4];		/* u=rwx,g=rwx,o=rwx */
  int i;

  i = 0;
  if ((um & S_IRUSR) == 0)
    ubits[i++] = 'r';
  if ((um & S_IWUSR) == 0)
    ubits[i++] = 'w';
  if ((um & S_IXUSR) == 0)
    ubits[i++] = 'x';
  ubits[i] = '\0';

  i = 0;
  if ((um & S_IRGRP) == 0)
    gbits[i++] = 'r';
  if ((um & S_IWGRP) == 0)
    gbits[i++] = 'w';
  if ((um & S_IXGRP) == 0)
    gbits[i++] = 'x';
  gbits[i] = '\0';

  i = 0;
  if ((um & S_IROTH) == 0)
    obits[i++] = 'r';
  if ((um & S_IWOTH) == 0)
    obits[i++] = 'w';
  if ((um & S_IXOTH) == 0)
    obits[i++] = 'x';
  obits[i] = '\0';

  printf ("u=%s,g=%s,o=%s\n", ubits, gbits, obits);
}

/* Set the umask from a symbolic mode string similar to that accepted
   by chmod.  If the -S argument is given, then print the umask in a
   symbolic form. */
static int
symbolic_umask (list)
     WORD_LIST *list;
{
  int um, umc, c;
  int who, op, perm, mask;
  char *s;

  /* Get the initial umask.  Don't change it yet. */
  um = umask (022);
  umask (um);

  /* All work below is done with the complement of the umask -- its
     more intuitive and easier to deal with.  It is complemented
     again before being returned. */
  umc = ~um;

  s = list->word->word;

  for (;;)
    {
      who = op = perm = mask = 0;

      /* Parse the `who' portion of the symbolic mode clause. */
      while (member (*s, "agou"))
        {
	  switch (c = *s++)
	    {
	      case 'u':
	        who |= S_IRWXU;
	        continue;
	      case 'g':
	        who |= S_IRWXG;
	        continue;
	      case 'o':
	        who |= S_IRWXO;
	        continue;
	      case 'a':
	        who |= S_IRWXU | S_IRWXG | S_IRWXO;
	        continue;
	      default:
	        break;
	    }
	}

      /* The operation is now sitting in *s. */
      op = *s++;
      switch (op)
	{
	  case '+':
	  case '-':
	  case '=':
	    break;
	  default:
	    builtin_error ("bad symbolic mode operator: %c", op);
	    return (-1);
	}

      /* Parse out the `perm' section of the symbolic mode clause. */
      while (member (*s, "rwx"))
	{
	  c = *s++;

	  switch (c)
	    {
	      case 'r':
		perm |= S_IRUGO;
		break;

	      case 'w':
		perm |= S_IWUGO;
		break;

	      case 'x':
		perm |= S_IXUGO;
		break;
	    }
	}

      /* Now perform the operation or return an error for a
	 bad permission string. */
      if (!*s || *s == ',')
	{
	  if (who)
	    perm &= who;

	  switch (op)
	    {
	      case '+':
	        umc |= perm;
	        break;

	      case '-':
	        umc &= ~perm;
	        break;

	      case '=':
	        umc &= ~who;
	        umc |= perm;
	        break;

	      default:
	      	builtin_error ("bad operation character: %c", op);
	      	return (-1);
	    }

	  if (!*s)
	    {
	      um = ~umc & 0777;
	      break;
	    }
	  else
	    s++;	/* skip past ',' */
	}
      else
	{
	  builtin_error ("bad character in symbolic mode: %c", *s);
	  return (-1);
	}
    }
  return (um);
}
