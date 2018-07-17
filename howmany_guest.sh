#!/bin/bash

SCRIPT_DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

HOSTNAME="$( hostname -s )"

if [ "${HOSTNAME}" != "serotonin" ]; then
    echo "This script needs to be run from serotonin"
    exit 1
fi

# shellcheck source=/dev/null
source "${SCRIPT_DIR}/.venv/bin/activate"

pushd "${SCRIPT_DIR}" > /dev/null || exit 2

pushd "data" > /dev/null || exit 2

sudo scp ala:/var/db/dhcpd/dhcpd.leases .

popd > /dev/null || exit 2

./howmany_guest.py -f data/dhcpd.leases

popd > /dev/null || exit 2

deactivate

exit 0
