#!/bin/bash
set -e

echo "[entrypoint] Setting CKAN configuration..."

LANG_VALUE=${CKAN_LANG:-en}
HARVEST_HOSTNAME=${HARVEST_MQ_HOSTNAME:-redis}

# Correct CKAN language key
ckan config-tool /srv/app/ckan.ini "ckan.locale_default = $LANG_VALUE"

# Enable DCAT RDF endpoints and set profiles
ckan config-tool /srv/app/ckan.ini "ckanext.dcat.enable_rdf_endpoints = true"
ckan config-tool /srv/app/ckan.ini "ckanext.dcat.rdf.profiles = euro_dcat_ap"

# Harvest: use Redis Kombu backend
ckan config-tool /srv/app/ckan.ini "ckan.harvest.mq.type = redis"
ckan config-tool /srv/app/ckan.ini "ckan.harvest.mq.redis.url = redis://$HARVEST_HOSTNAME:6379/0"

echo "[entrypoint] Configuration applied successfully."

# echo "[entrypoint] Initializing CKAN database..."
# if ckan db init; then
#     echo "[entrypoint] Database initialized successfully."
# else
#     echo "[entrypoint] WARNING: Database init failed or already done."
# fi

# echo "[entrypoint] Starting CKAN development server..."
# exec ckan run --host=0.0.0.0 --port=5000
