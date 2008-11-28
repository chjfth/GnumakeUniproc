This project checks out its sub-projects from both SVN repository and CVS repository.

The key point is, for a sub-project <refname>,
* If <refname>_cvsRoot_forMakefiles is non-null, CVS checkout is used.
# Else if <refname>_svnUrl_forMakefiles is non-null, SVN checkout is used.
