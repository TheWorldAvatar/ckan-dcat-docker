#!/bin/sh
set -e
INI="/srv/app/ckan.ini"
[ -f "$INI" ] && sed -i '/^[[:space:]]*lang[[:space:]]*=.*/d' "$INI" || true
