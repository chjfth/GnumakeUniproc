/* setattr.c, created from setattr.def. */
//#line 23 "./setattr.def"

#include "../shell.h"
#include "common.h"
#include "bashgetopt.h"

extern int array_needs_making;
extern char *this_command_name;
extern char * nt_remove_cr_string(char * str);

//#line 42 "./setattr.def"

/* For each variable name in LIST, make that variable appear in the
   environment passed to simple commands.  If there is no LIST, then
   print all such variables.  An argument of `-n' says to remove the
   exported attribute from variables named in LIST.  An argument of
  -f indicates that the names present in LIST refer to functions. */
export_builtin (list)
     register WORD_LIST *list;
{
  return (set_or_show_attributes (list, att_exported));
}

//#line 65 "./setattr.def"

/* For each variable name in LIST, make that variable readonly.  Given an
   empty LIST, print out all existing readonly variables. */
readonly_builtin (list)
     register WORD_LIST *list;
{
  return (set_or_show_attributes (list, att_readonly));
}

/* For each variable name in LIST, make that variable have the specified
   ATTRIBUTE.  An arg of `-n' says to remove the attribute from the the
   remaining names in LIST. */
int
set_or_show_attributes (list, attribute)
     register WORD_LIST *list;
     int attribute;
{
  register SHELL_VAR *var;
  int assign, undo = 0, functions_only = 0, any_failed = 0, opt;

  /* Read arguments from the front of the list. */
  reset_internal_getopt ();
  while ((opt = internal_getopt (list, "nfp")) != -1)
    {
      switch (opt)
	{
	  case 'n':
	    undo = 1;
	    break;
	  case 'f':
	    functions_only = 1;
	    break;
	  case 'p':
	    break;
	  default:
	    builtin_error ("usage: %s [-nfp] [varname]", this_command_name);
	    return (EX_USAGE);
	}
    }
  list = loptend;

  if (list)
    {
      if (attribute & att_exported)
	array_needs_making = 1;

      while (list)
	{
#ifndef __NT_VC__
	  register char *name = list->word->word;
#else
	  register char *name = nt_remove_cr_string(list->word->word);
#endif

	  if (functions_only)
	    {
	      var = find_function (name);
	      if (!var)
		{
		  builtin_error ("%s: not a function", name);
		  any_failed++;
		}
	      else
		{
		  if (undo)
		    var->attributes &= ~attribute;
		  else
		    var->attributes |= attribute;
		}
	      list = list->next;
	      if (attribute == att_exported)
		array_needs_making++;
	      continue;
	    }

	  assign = assignment (name);

          if (assign)
	    name[assign] = '\0';
	  if (legal_identifier (name) == 0)
	    {
	      builtin_error ("%s: not a legal variable name", name);
	      any_failed++;
	      list = list->next;
	      continue;
	    }

	  if (assign)
	    {
	      name[assign] = '=';
	      /* This word has already been expanded once with command
		 and parameter expansion.  Call do_assignment_no_expand (),
		 which does not do command or parameter substitution. */
	      do_assignment_no_expand (name);
	      name[assign] = '\0';
	    }

	  if (undo)
	    {
	      var = find_variable (name);
	      if (var)
		var->attributes &= ~attribute;
	    }
	  else
	    {
	      SHELL_VAR *find_tempenv_variable (), *tv;

	      if (tv = find_tempenv_variable (name))
		{
		  var = bind_variable (tv->name, tv->value);
		  dispose_variable (tv);
		}
	      else
		var = find_variable (name);

	      if (!var)
		{
		  var = bind_variable (name, (char *)NULL);
		  var->attributes |= att_invisible;
		}

	      var->attributes |= attribute;
	    }

	  array_needs_making++;	/* XXX */
	  list = list->next;
	}
    }
  else
    {
      SHELL_VAR **variable_list;
      register int i;

      if ((attribute & att_function) || functions_only)
	{
	  variable_list = all_shell_functions ();
	  if (attribute != att_function)
	    attribute &= ~att_function;	/* so declare -xf works, for example */
	}
      else
	variable_list = all_shell_variables ();

      if (variable_list)
	{
	  for (i = 0; var = variable_list[i]; i++)
	    {
	      if ((var->attributes & attribute) && !invisible_p (var))
		{
		  char flags[6];

		  flags[0] = '\0';

		  if (exported_p (var))
		    strcat (flags, "x");

		  if (readonly_p (var))
		    strcat (flags, "r");

		  if (function_p (var))
		    strcat (flags, "f");

		  if (integer_p (var))
		    strcat (flags, "i");

		  if (flags[0])
		    {
		      printf ("declare -%s ", flags);

		      if (!function_p (var))
			{
			  char *x = double_quote (value_cell (var));
			  printf ("%s=%s\n", var->name, x);
			  free (x);
			}
		      else
			{
			  char *named_function_string ();

			  printf ("%s\n", named_function_string
				  (var->name, function_cell (var), 1));
			}
		    }
		}
	    }
	  free (variable_list);
	}
    }
  return (any_failed == 0 ? EXECUTION_SUCCESS : EXECUTION_FAILURE);
}
