/usr/bin/pylupdate5 $(find src -name '*.py' -o -name '*.ui') -noobsolete -verbose $(for tr in "$@"; do echo "-ts translations/$tr.ts"; done)
/usr/bin/lrelease $(find src -name '*.ts')
