/* source.c, created from source.def. */

/* source.c - Implements the `.' and `source' builtins. */

#include <sys/types.h>
#include <sys/file.h>
#include <errno.h>

#if defined (HAVE_STRING_H)
#  include <string.h>
#else /* !HAVE_STRING_H */
#  include <strings.h>
#endif /* !HAVE_STRING_H */

#include "../shell.h"
#include "../posixstat.h"
#include "../filecntl.h"
#include "../execute_cmd.h"

/* Not all systems declare ERRNO in errno.h... and some systems #define it! */
#if !defined (errno)
extern int errno;
#endif /* !errno */

/* Variables used here but defined in other files. */
extern int return_catch_flag, return_catch_value;
extern jmp_buf return_catch;
extern int posixly_correct;
extern int interactive, interactive_shell;

/* How many `levels' of sourced files we have. */
int sourcelevel = 0;

/* If this . script is supplied arguments, we save the dollar vars and
   replace them with the script arguments for the duration of the script's
   execution.  If the script does not change the dollar vars, we restore
   what we saved.  If the dollar vars are changed in the script, we leave
   the new values alone and free the saved values. */
static void
maybe_pop_dollar_vars ()
{
  if (dollar_vars_changed ())
    {
      dispose_saved_dollar_vars ();
      set_dollar_vars_unchanged ();
    }
  else
    pop_dollar_vars ();
}

/* Read and execute commands from the file passed as argument.  Guess what.
   This cannot be done in a subshell, since things like variable assignments
   take place in there.  So, I open the file, place it into a large string,
   close the file, and then execute the string. */
source_builtin (list)
     WORD_LIST *list;
{
  int result, return_val;

  /* Assume the best. */
  result = EXECUTION_SUCCESS;

  if (list)
    {
      char *string, *filename;
      struct stat finfo;
      int fd, tt;

      filename = find_path_file (list->word->word);
      if (!filename)
	filename = savestring (list->word->word);

      if (((fd = OPEN (filename, O_RDONLY)) < 0) || (fstat (fd, &finfo) < 0))
         goto file_error_exit;
      
      string = (char *)xmalloc (1 + (int)finfo.st_size);
      tt = read (fd, string, finfo.st_size);
      string[finfo.st_size] = '\0';
      
#ifdef __NT_VC__
      nt_remove_cr(string,finfo.st_size);
#endif
      
      /* Close the open file, preserving the state of errno. */
      { int temp = errno; CLOSE (fd); errno = temp; }

      if (tt != finfo.st_size)
	{
	  free (string);

	file_error_exit:
	  file_error (filename);
	  free (filename);

	  /* POSIX shells exit if non-interactive and file error. */
	  if (posixly_correct && !interactive_shell)
	    LONGJMP (top_level, EXITPROG);

	  return (EXECUTION_FAILURE);
	}

      if (tt > 80)
	tt = 80;

      if (check_binary_file ((unsigned char *)string, tt))
	{
	  free (string);
	  builtin_error ("%s: cannot execute binary fileZ", filename);
	  free (filename);
	  return (EX_BINARY_FILE);
	}

      begin_unwind_frame ("File Sourcing");

      if (list->next)
	{
	  push_dollar_vars ();
	  add_unwind_protect ((Function *)maybe_pop_dollar_vars, (char *)NULL);
	  remember_args (list->next, 1);
	}

      unwind_protect_int (return_catch_flag);
      unwind_protect_jmp_buf (return_catch);
      unwind_protect_int (interactive);
      unwind_protect_int (sourcelevel);
      add_unwind_protect ((Function *)xfree, filename);
      interactive = 0;
      sourcelevel++;

      set_dollar_vars_unchanged ();

      return_catch_flag++;
      /*return_val = SETJMP(return_catch);*/
      SETJMP(return_val, return_catch);

      if (return_val)
	parse_and_execute_cleanup ();
      else
	result = parse_and_execute (string, filename, -1);

      run_unwind_frame ("File Sourcing");

      /* If RETURN_VAL is non-zero, then we return the value given
	 to return_builtin (), since that is how we got here. */
      if (return_val)
	result = return_catch_value;
    }
  return (result);
}
