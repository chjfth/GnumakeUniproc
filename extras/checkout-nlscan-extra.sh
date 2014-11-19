#!/bin/bash

mydir=${0%/*}

svn co https://nlssvn/svnreps/makingsys/GMU-addons/trunk/nlscan $(realpath $mydir/../nlscan)

