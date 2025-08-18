#!/bin/bash
set -e

echo ">> Enabling DCAT, Harvester plugins..."
ckan config-tool ${APP_DIR}/ckan.ini "ckan.plugins = ${CKAN__PLUGINS}"

if [ -n "${CKAN__DCAT__APIHOST}" ]; then
  ckan config-tool ${APP_DIR}/ckan.ini "ckanext.dcat.apihost = ${CKAN__DCAT__APIHOST}"
else
  ckan config-tool ${APP_DIR}/ckan.ini "ckanext.dcat.apihost = https://localhost:8443"
fi

ckan config-tool ${APP_DIR}/ckan.ini "ckan.secret_keys = ${SECRET_KEY}"

echo ">> DCAT, Harvester config done!"
exec env SECRET_KEY="${SECRET_KEY}" "$@"
