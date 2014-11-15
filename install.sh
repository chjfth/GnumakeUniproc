#!/bin/bash

${0%/*}/GMU-main/install-exe.sh "$@"

if [ "$?" != 0 ]; then exit $?; fi

