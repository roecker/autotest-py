#!/bin/bash 
#
# file created: Di, 11 Dez 2007  12:57
# latest changes: Mi, 26. Aug 2015  13:47
#
# _VMware: server=d1
# _VMware: client=c1
#
############################################
getSettings
rc=0
############################################
info "new test \"$(dirname $0)\" started..."

echo "using server (orbiter): $server"

info "test \"$0\" finished."
exit $rc

