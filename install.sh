#!/bin/bash

${0%/*}/GMU-main/install-exe.sh "$@"

if [ "$?" != 0 ]; then exit $?; fi

echo ""
echo "GMU installed OK!"
echo "Remember to 'source ${0%/*}/gmuenv.sc' every time you login to your shell to setup GMU env! You can do it in '.bashrc' for convenience."
