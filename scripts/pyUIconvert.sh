find . -name '*.ui' -exec sh -c '/usr/bin/pyuic5 "$1" -o "$(echo "$1" | sed "s/\\.ui/\\.py/")"' _ {} \;
