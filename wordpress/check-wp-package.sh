#!/usr/bin/env bash

set -eo pipefail

workdir='/var/www/html'

if [[ -e $workdir/installer.php ]]

then

    echo "Duplicator package found."
    echo "Executing $@"
    exec "$@"

else
    echo "Duplicator package not found"
    echo "Running image original entrypoint"
    docker-entrypoint.sh $1

fi
