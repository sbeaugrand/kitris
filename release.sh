#!/bin/bash
# ---------------------------------------------------------------------------- #
## \file release.sh
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
dname="cn=SBeaugrand, ou=SBeaugrand Mobility, o=SBeaugrand, c=FR"
kpath=/mnt/crypted/keystores
kstore=$kpath/sbkeystore.keystore

if [ -z "$1" ]; then
    echo "Usage: `basename $0` <alias>"
    exit 1
fi
ralias="$1"
file="$kpath/$ralias.sh"

if [ ! -f $kstore ]; then
    mkdir $kpath || exit 1
    echo -n "pass ? "
    read pass
    cat >"$file" <<EOF
export P4A_RELEASE_KEYSTORE=$kstore
export P4A_RELEASE_KEYSTORE_PASSWD=$pass
export P4A_RELEASE_KEYALIAS_PASSWD=$pass
export P4A_RELEASE_KEYALIAS="$ralias"
EOF
    source "$file"
    keytool -genkeypair -dname "$dname"\
     -keystore $kstore -storepass $P4A_RELEASE_KEYSTORE_PASSWD\
     -alias "$ralias" -keypass $P4A_RELEASE_KEYALIAS_PASSWD\
     -keyalg RSA -validity 36500 -storetype pkcs12
else
    source "$file" || exit 1
fi

buildozer --profile release android release
