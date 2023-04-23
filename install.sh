# ---------------------------------------------------------------------------- #
## \file install.sh
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
path=$(dirname `readlink -f $0`)
file=${1:-$HOME/.local/share/applications/kitris.desktop}

cat >$file <<EOF
[Desktop Entry]
Name=kitris
Comment=Tetris game with kivy and bluetooth
Icon=$path/data/icon.png
Exec=$path/main.py
Type=Application
Terminal=false
Categories=Game;
Path=$path
StartupNotify=false
EOF
