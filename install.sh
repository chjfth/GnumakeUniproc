#!/bin/bash

${0%/*}/GMU-main/install-exe.sh "$@"

if [ "$?" != 0 ]; then exit $?; fi

echo ""
echo "GMU installed OK!"
echo "Remember to add '${0%/*}/bin' to your PATH in order to execute umake commands."
