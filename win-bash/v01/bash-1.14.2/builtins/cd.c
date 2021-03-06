/* cd.c, created from cd.def. */
#include <stdio.h>
#include <sys/param.h>

#if defined (HAVE_STRING_H)
#  include <string.h>
#else /* !HAVE_STRING_H */
#  include <strings.h>
#endif /* !HAVE_STRING_H */

#include <errno.h>
#include <tilde/tilde.h>

#include "../shell.h"
#include "../flags.h"
#include "../maxpath.h"
#include "common.h"

#if !defined (errno)
extern int errno;
#endif /* !errno */

static int change_to_directory (), cd_to_string ();

/* This builtin is ultimately the way that all user-visible commands should
   change the current working directory.  It is called by cd_to_string (),
   so the programming interface is simple, and it handles errors and
   restrictions properly. */
int
cd_builtin (list)
     WORD_LIST *list;
{
  char *dirname;

#if defined (RESTRICTED_SHELL)
  if (restricted)
    {
      builtin_error ("restricted");
      return (EXECUTION_FAILURE);
    }
#endif /* RESTRICTED_SHELL */

  if (list)
    {
      char *extract_colon_unit ();
      const char *path_string = get_string_value ("CDPATH");
      char *path;
      int path_index = 0, dirlen, pathlen;

      dirname = list->word->word;

      if (path_string && !absolute_pathname (dirname))
	{
	  while ((path = extract_colon_unit (path_string, &path_index)))
	    {
	      char *dir;

	      if (*path == '~')
		{
		  char *te_string = tilde_expand (path);

		  free (path);
		  path = te_string;
		}

	      if (!*path)
		{
		  free (path);
		  path = xmalloc (2);
		  path[0] = '.';	/* by definition. */
		  path[1] = '\0';
		}

	      dirlen = strlen (dirname);
	      pathlen = strlen (path);
	      dir = xmalloc (2 + dirlen + pathlen);
	      strcpy (dir, path);
	      if (path[pathlen - 1] != '/')
	        {
	          dir[pathlen++] = '/';
	          dir[pathlen] = '\0';
	        }
	      strcpy (dir + pathlen, dirname);
	      free (path);

	      if (change_to_directory (dir))
		{
		  /* replaces (strncmp (dir, "./", 2) != 0) */
		  if (dir[0] != '.' || dir[1] != '/')
		    printf ("%s\n", dir);

		  free (dir);
		  goto bind_and_exit;
		}
	      else
		free (dir);
	    }
	}

      if (!change_to_directory (dirname))
	{
	  /* Maybe this is `cd -', equivalent to `cd $OLDPWD' */
	  if (dirname[0] == '-' && dirname[1] == '\0')
	    {
	      char *t = get_string_value ("OLDPWD");

	      if (t && change_to_directory (t))
		goto bind_and_exit;
	    }

	  /* If the user requests it, then perhaps this is the name of
	     a shell variable, whose value contains the directory to
	     change to.  If that is the case, then change to that
	     directory. */
	  if (find_variable ("cdable_vars"))
	    {
	      char *t = get_string_value (dirname);

	      if (t && change_to_directory (t))
		{
		  printf ("%s\n", t);
		  goto bind_and_exit;
		}
	    }

	  file_error (dirname);
	  return (EXECUTION_FAILURE);
	}
      goto bind_and_exit;
    }
  else
    {
      dirname = get_string_value ("HOME");

      if (!dirname)
	return (EXECUTION_FAILURE);

      if (!change_to_directory (dirname))
	{
	  file_error (dirname);
	  return (EXECUTION_FAILURE);
	}

    bind_and_exit:
      {
	char *directory;

	directory = get_working_directory ("cd");

	bind_variable ("OLDPWD", get_string_value ("PWD"));
	bind_variable ("PWD", directory);

	FREE (directory);
      }
      return (EXECUTION_SUCCESS);
    }
}

/* Non-zero means that pwd always give verbatim directory, regardless of
   symbolic link following. */
static int verbatim_pwd;

/* Print the name of the current working directory. */
pwd_builtin (list)
     WORD_LIST *list;
{
  char *directory, *s;

#if 0
  no_args (list);
#else
  verbatim_pwd = no_symbolic_links;
  if (list && (s = list->word->word) && s[0] == '-' && s[1] == 'P' && !s[2])
    verbatim_pwd = 1;
#endif

  if (verbatim_pwd)
    {
      char *buffer = xmalloc (MAXPATHLEN);
      directory = getwd (buffer);

      if (!directory)
	{
	  builtin_error ("%s", buffer);
	  free (buffer);
	}
    }
  else
    directory = get_working_directory ("pwd");

  if (directory)
    {
      printf ("%s\n", directory);
      fflush (stdout);
      free (directory);
      return (EXECUTION_SUCCESS);
    }
  else
    return (EXECUTION_FAILURE);
}

#if defined (PUSHD_AND_POPD)
/* Some useful commands whose behaviour has been observed in Csh. */

/* The list of remembered directories. */
static char **pushd_directory_list = (char **)NULL;

/* Number of existing slots in this list. */
static int directory_list_size = 0;

/* Offset to the end of the list. */
static int directory_list_offset = 0;

pushd_builtin (list)
     WORD_LIST *list;
{
  char *temp, *current_directory;
  int j = directory_list_offset - 1;
  char direction = '+';

  /* If there is no argument list then switch current and
     top of list. */
  if (!list)
    {
      if (!directory_list_offset)
	{
	  builtin_error ("No other directory");
	  return (EXECUTION_FAILURE);
	}

      current_directory = get_working_directory ("pushd");
      if (!current_directory)
	return (EXECUTION_FAILURE);

      temp = pushd_directory_list[j];
      pushd_directory_list[j] = current_directory;
      goto change_to_temp;
    }
  else
    {
      direction = *(list->word->word);
      if (direction == '+' || direction == '-')
	{
	  int num;
	  if (1 == sscanf (&(list->word->word)[1], "%d", &num))
	    {
	      if (direction == '-')
		num = directory_list_offset - num;

	      if (num > directory_list_offset || num < 0)
		{
		  if (!directory_list_offset)
		    builtin_error ("Directory stack empty");
		  else
		    builtin_error ("Stack contains only %d directories",
				    directory_list_offset + 1);
		  return (EXECUTION_FAILURE);
		}
	      else
		{
		  /* Rotate the stack num times.  Remember, the
		     current directory acts like it is part of the
		     stack. */
		  temp = get_working_directory ("pushd");

		  if (!num)
		    goto change_to_temp;

		  do
		    {
		      char *top =
			pushd_directory_list[directory_list_offset - 1];

		      for (j = directory_list_offset - 2; j > -1; j--)
			pushd_directory_list[j + 1] = pushd_directory_list[j];

		      pushd_directory_list[j + 1] = temp;

		      temp = top;
		      num--;
		    }
		  while (num);

		  temp = savestring (temp);
		change_to_temp:
		  {
		    int tt = EXECUTION_FAILURE;

		    if (temp)
		      {
			tt = cd_to_string (temp);
			free (temp);
		      }

		    if ((tt == EXECUTION_SUCCESS))
		      dirs_builtin ((WORD_LIST *)NULL);

		    return (tt);
		  }
		}
	    }
	}

      /* Change to the directory in list->word->word.  Save the current
	 directory on the top of the stack. */
      current_directory = get_working_directory ("pushd");
      if (!current_directory)
	return (EXECUTION_FAILURE);

      if (cd_builtin (list) == EXECUTION_SUCCESS)
	{
	  if (directory_list_offset == directory_list_size)
	    {
	      pushd_directory_list = (char **)
		xrealloc (pushd_directory_list,
			  (directory_list_size += 10) * sizeof (char *));
	    }
	  pushd_directory_list[directory_list_offset++] = current_directory;

	  dirs_builtin ((WORD_LIST *)NULL);

	  return (EXECUTION_SUCCESS);
	}
      else
	{
	  free (current_directory);
	  return (EXECUTION_FAILURE);
	}
    }
}
#endif /* PUSHD_AND_POPD */

#if defined (PUSHD_AND_POPD)
/* Print the current list of directories on the directory stack. */
dirs_builtin (list)
     WORD_LIST *list;
{
  int i, format, desired_index, index_flag;
  char *temp, *w;

  format = index_flag = 0;
  desired_index = -1;
  /* Maybe do long form or print specific dir stack entry? */
  while (list)
    {
      if (strcmp (list->word->word, "-l") == 0)
	{
	  format++;
	  list = list->next;
	}
      else if (*list->word->word == '+' && all_digits (list->word->word + 1))
	{
	  w = list->word->word + 1;
	  index_flag = 1;
	  i = atoi (w);
	  /* dirs +0 prints the current working directory. */
	  if (i == 0)
	    desired_index = i;
	  else if (i == directory_list_offset)
	    {
	      desired_index = 0;
	      index_flag = 2;
	    }
	  else
	    desired_index = directory_list_offset - i;
	  list = list->next;
	}
      else if (*list->word->word == '-' && all_digits (list->word->word + 1))
	{
	  w = list->word->word + 1;
	  i = atoi (w);
	  index_flag = 2;
	  /* dirs -X where X is directory_list_offset prints the current
	     working directory. */
	  if (i == directory_list_offset)
	    {
	      index_flag = 1;
	      desired_index = 0;
	    }
	  else
	    desired_index = i;
	  list = list->next;
	}
      else
	{
	  bad_option (list->word->word);
	  return (EXECUTION_FAILURE);
	}
    }

  if (index_flag && (desired_index < 0 || desired_index > directory_list_offset))
    {
      if (directory_list_offset == 0)
	builtin_error ("directory stack empty");
      else
	builtin_error ("%s: bad directory stack index", w);
      return (EXECUTION_FAILURE);
    }

  /* The first directory printed is always the current working directory. */
  if (!index_flag || (index_flag == 1 && desired_index == 0))
    {
      temp = get_working_directory ("dirs");
      if (!temp)
	temp = savestring ("<no directory>");
      printf ("%s", format ? temp : polite_directory_format (temp));
      free (temp);
      if (index_flag)
	{
	  putchar ('\n');
	  return EXECUTION_SUCCESS;
	}
    }

#define DIRSTACK_ENTRY(i) \
	format ? pushd_directory_list[i] \
	       : polite_directory_format (pushd_directory_list[i])

  /* Now print the requested directory stack entries. */
  if (index_flag)
    printf ("%s", DIRSTACK_ENTRY (desired_index));
  else
    for (i = (directory_list_offset - 1); i > -1; i--)
      printf (" %s", DIRSTACK_ENTRY (i));

  putchar ('\n');
  fflush (stdout);
  return (EXECUTION_SUCCESS);
}
#endif /* PUSHD_AND_POPD */

#if defined (PUSHD_AND_POPD)
/* Pop the directory stack, and then change to the new top of the stack.
   If LIST is non-null it should consist of a word +N or -N, which says
   what element to delete from the stack.  The default is the top one. */
popd_builtin (list)
     WORD_LIST *list;
{
  register int i;
  int which = 0;
  char direction = '+';

  if (list)
    {
      direction = *(list->word->word);

      if ((direction != '+' && direction != '-') ||
	  (1 != sscanf (&((list->word->word)[1]), "%d", &which)))
	{
	  builtin_error ("bad arg `%s'", list->word->word);
	  return (EXECUTION_FAILURE);
	}
    }

  if (which > directory_list_offset || (!directory_list_offset && !which))
    {
      if (!directory_list_offset)
	builtin_error ("Directory stack empty");
      else
	builtin_error ("Stack contains only %d directories",
			directory_list_offset + 1);
      return (EXECUTION_FAILURE);
    }

  /* Handle case of no specification, or top of stack specification. */
  if ((direction == '+' && which == 0) ||
      (direction == '-' && which == directory_list_offset))
    {
      i = cd_to_string (pushd_directory_list[directory_list_offset - 1]);
      if (i != EXECUTION_SUCCESS)
	return (i);
      free (pushd_directory_list[--directory_list_offset]);
    }
  else
    {
      /* Since an offset other than the top directory was specified,
	 remove that directory from the list and shift the remainder
	 of the list into place. */

      if (direction == '+')
	i = directory_list_offset - which;
      else
	i = which;

      free (pushd_directory_list[i]);
      directory_list_offset--;

      /* Shift the remainder of the list into place. */
      for (; i < directory_list_offset; i++)
	pushd_directory_list[i] = pushd_directory_list[i + 1];
    }

  dirs_builtin ((WORD_LIST *)NULL);

  return (EXECUTION_SUCCESS);
}
#endif /* PUSHD_AND_POPD */

/* Do the work of changing to the directory NEWDIR.  Handle symbolic
   link following, etc. */

static int
change_to_directory (newdir)
     char *newdir;
{
  char *t;

  if (!no_symbolic_links)
    {
      int chdir_return = 0;
      char *tdir = (char *)NULL;

      if (!the_current_working_directory)
	{
	  t = get_working_directory ("cd_links");
	  FREE (t);
	}

      if (the_current_working_directory)
	t = make_absolute (newdir, the_current_working_directory);
      else
	t = savestring (newdir);

      /* TDIR is the canonicalized absolute pathname of the NEWDIR. */
      tdir = canonicalize_pathname (t);

      /* Use the canonicalized version of NEWDIR, or, if canonicalization
	 failed, use the non-canonical form. */
      if (tdir && *tdir)
	free (t);
      else
	{
	  FREE (tdir);

	  tdir = t;
	}

   if (chdir (tdir) < 0)
	{
	  int err;

	  chdir_return = 0;
	  free (tdir);

	  err = errno;

	  /* We failed changing to the canonicalized directory name.  Try
	     what the user passed verbatim.  If we succeed, reinitialize
	     the_current_working_directory. */
	  if (chdir (newdir) == 0)
	    {
	      chdir_return = 1;
	      if (the_current_working_directory)
		{
		  free (the_current_working_directory);
		  the_current_working_directory = (char *)NULL;
		}

	      tdir = get_working_directory ("cd");
	      FREE (tdir);
	    }
	  else
	    errno = err;
	}
      else
	{
	  chdir_return = 1;

	  FREE (the_current_working_directory);
	  the_current_working_directory = tdir;
	}

      return (chdir_return);
    }
  else
    {
      if (chdir (newdir) < 0)
	return (0);
      else
	return (1);
    }
}

/* Switch to the directory in NAME.  This uses the cd_builtin to do the work,
   so if the result is EXECUTION_FAILURE then an error message has already
   been printed. */
static int
cd_to_string (name)
     char *name;
{
  WORD_LIST *tlist = make_word_list (make_word (name), NULL);
  int result = (cd_builtin (tlist));
  dispose_words (tlist);
  return (result);
}

// 2009-12-30 Chj: add true, false builtin
// Thanks to http://files.linjian.org/articles/bash_study/bash_linjian.html

int
true_builtin (WORD_LIST *list)
{
	return 0;
}

int
false_builtin (WORD_LIST *list)
{
	return 1;
}
