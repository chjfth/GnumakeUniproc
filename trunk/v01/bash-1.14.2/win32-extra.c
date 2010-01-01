#include <windows.h>
#include <win32-extra.h>

////////////// Chj:

int execute_wincmd(char *wincmd)
{
	DWORD process_exitcode = 0;
	STARTUPINFO sti = { sizeof(STARTUPINFO) };
	PROCESS_INFORMATION psi;
	BOOL b = CreateProcess(NULL, wincmd, NULL, NULL,
		FALSE,
		0,
		NULL, NULL,
		&sti, &psi);
	if(b)
	{
		WaitForSingleObject(psi.hProcess, INFINITE);
		GetExitCodeProcess(psi.hProcess, &process_exitcode);
		
		CloseHandle(psi.hThread);
		CloseHandle(psi.hProcess);
		return process_exitcode;
	}
	else
		return GetLastError();
}

// 2010-01-01 Chj: make_command_line() is borrowed from GNU make 3.81, sub_proc.c ,
// to convert argc,argv[] represented command params into a CreateProcess command line.
// The convering rule is documented at http://msdn.microsoft.com/en-us/library/17w5ykft.aspx
/*
 * Description:
 *	 Create a command line buffer to pass to CreateProcess
 *
 * Returns:  the buffer or NULL for failure
 *	Shell case:  sh_name a:/full/path/to/script argv[1] argv[2] ...
 *  Otherwise:   argv[0] argv[1] argv[2] ...
 *
 * Notes/Dependencies:
 *   CreateProcess does not take an argv, so this command creates a
 *   command line for the executable.
 */

char *
make_command_line( char *shell_name, char *full_exec_path, char **argv)
{
	int		argc = 0;
	char**		argvi;
	int*		enclose_in_quotes = NULL;
	int*		enclose_in_quotes_i;
	unsigned int	bytes_required = 0;
	char*		command_line;
	char*		command_line_i;
	int  cygwin_mode = 0; /* HAVE_CYGWIN_SHELL */
	int have_sh = 0; /* HAVE_CYGWIN_SHELL */

#ifdef HAVE_CYGWIN_SHELL
	have_sh = (shell_name != NULL || strstr(full_exec_path, "sh.exe"));
	cygwin_mode = 1;
#endif

	if (shell_name && full_exec_path) {
		bytes_required
		  = strlen(shell_name) + 1 + strlen(full_exec_path);
		/*
		 * Skip argv[0] if any, when shell_name is given.
		 */
		if (*argv) argv++;
		/*
		 * Add one for the intervening space.
		 */
		if (*argv) bytes_required++;
	}

	argvi = argv;
	while (*(argvi++)) argc++;

	if (argc) {
		enclose_in_quotes = (int*) calloc(1, argc * sizeof(int));

		if (!enclose_in_quotes) {
			return NULL;
		}
	}

	/* We have to make one pass through each argv[i] to see if we need
	 * to enclose it in ", so we might as well figure out how much
	 * memory we'll need on the same pass.
	 */

	argvi = argv;
	enclose_in_quotes_i = enclose_in_quotes;
	while(*argvi) {
		char* p = *argvi;
		unsigned int backslash_count = 0;

		/*
		 * We have to enclose empty arguments in ".
		 */
		if (!(*p)) *enclose_in_quotes_i = 1;

		while(*p) {
			switch (*p) {
			case '\"':
				/*
				 * We have to insert a backslash for each "
				 * and each \ that precedes the ".
				 */
				bytes_required += (backslash_count + 1);
				backslash_count = 0;
				break;

#if !defined(HAVE_MKS_SHELL) && !defined(HAVE_CYGWIN_SHELL)
			case '\\':
				backslash_count++;
				break;
#endif
	/*
	 * At one time we set *enclose_in_quotes_i for '*' or '?' to suppress
	 * wildcard expansion in programs linked with MSVC's SETARGV.OBJ so
	 * that argv in always equals argv out. This was removed.  Say you have
	 * such a program named glob.exe.  You enter
	 * glob '*'
	 * at the sh command prompt.  Obviously the intent is to make glob do the
	 * wildcarding instead of sh.  If we set *enclose_in_quotes_i for '*' or '?',
	 * then the command line that glob would see would be
	 * glob "*"
	 * and the _setargv in SETARGV.OBJ would _not_ expand the *.
	 */
			case ' ':
			case '\t':
				*enclose_in_quotes_i = 1;
				/* fall through */

			default:
				backslash_count = 0;
				break;
			}

			/*
			 * Add one for each character in argv[i].
			 */
			bytes_required++;

			p++;
		}

		if (*enclose_in_quotes_i) {
			/*
			 * Add one for each enclosing ",
			 * and one for each \ that precedes the
			 * closing ".
			 */
			bytes_required += (backslash_count + 2);
		}

		/*
		 * Add one for the intervening space.
		 */
		if (*(++argvi)) bytes_required++;
		enclose_in_quotes_i++;
	}

	/*
	 * Add one for the terminating NULL.
	 */
	bytes_required++;

	command_line = (char*) malloc(bytes_required);

	if (!command_line) {
		if (enclose_in_quotes) free(enclose_in_quotes);
		return NULL;
	}

	command_line_i = command_line;

	if (shell_name && full_exec_path) {
		while(*shell_name) {
			*(command_line_i++) = *(shell_name++);
		}

		*(command_line_i++) = ' ';

		while(*full_exec_path) {
			*(command_line_i++) = *(full_exec_path++);
		}

		if (*argv) {
			*(command_line_i++) = ' ';
		}
	}

	argvi = argv;
	enclose_in_quotes_i = enclose_in_quotes;

	while(*argvi) {
		char* p = *argvi;
		unsigned int backslash_count = 0;

		if (*enclose_in_quotes_i) {
			*(command_line_i++) = '\"';
		}

		while(*p) {
			if (*p == '\"') {
				if (cygwin_mode && have_sh) { /* HAVE_CYGWIN_SHELL */
					/* instead of a \", cygwin likes "" */
					*(command_line_i++) = '\"';
				} else {

				/*
				 * We have to insert a backslash for the "
				 * and each \ that precedes the ".
				 */
				backslash_count++;

				while(backslash_count) {
					*(command_line_i++) = '\\';
					backslash_count--;
				};
				}
#if !defined(HAVE_MKS_SHELL) && !defined(HAVE_CYGWIN_SHELL)
			} else if (*p == '\\') {
				backslash_count++;
			} else {
				backslash_count = 0;
#endif
			}

			/*
			 * Copy the character.
			 */
			*(command_line_i++) = *(p++);
		}

		if (*enclose_in_quotes_i) {
#if !defined(HAVE_MKS_SHELL) && !defined(HAVE_CYGWIN_SHELL)
			/*
			 * Add one \ for each \ that precedes the
			 * closing ".
			 */
			while(backslash_count--) {
				*(command_line_i++) = '\\';
			};
#endif
			*(command_line_i++) = '\"';
		}

		/*
		 * Append an intervening space.
		 */
		if (*(++argvi)) {
			*(command_line_i++) = ' ';
		}

		enclose_in_quotes_i++;
	}

	/*
	 * Append the terminating NULL.
	 */
	*command_line_i = '\0';

	if (enclose_in_quotes) free(enclose_in_quotes);
	return command_line;
}
