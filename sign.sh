#!/bin/bash

format_num() {
    local num=$(sed 's/\s+//g;s/[^0-9\.]//g;' <<< $1)
    echo "$num"
}

make clean
make dist
make reinstall

VERSION="$(format_num "$(python3 -m pyapa -v)")"
KEY="AB55927D"

gpg --default-key $KEY --armour --detach-sign dist/pyapa-$VERSION.tar.gz
