#ifndef __win32_extra_h_
#define __win32_extra_h_

int execute_wincmd(char *wincmd);

char *make_command_line( char *shell_name, char *full_exec_path, char **argv);

#endif
