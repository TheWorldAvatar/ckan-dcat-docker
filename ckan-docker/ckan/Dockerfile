FROM ckan/ckan-dev:2.11
USER root
# Install extensions
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-harvest.git#egg=ckanext-harvest' && \
    pip3 install -r ${APP_DIR}/src/ckanext-harvest/requirements.txt

RUN pip3 install -e 'git+https://github.com/ckan/ckanext-dcat.git@master#egg=ckanext-dcat' && \
    pip3 install -r https://raw.githubusercontent.com/ckan/ckanext-dcat/master/requirements.txt

# Copy entrypoint script
COPY --chown=ckan-sys:ckan-sys /docker-entrypoint.d/consumer-entrypoint.sh /srv/app/consumer-entrypoint.sh
RUN chmod +x /srv/app/consumer-entrypoint.sh

# Copy the CKAN config script
COPY --chown=ckan-sys:ckan-sys /docker-entrypoint.d/set_ckan_config.sh /srv/app/set_ckan_config.sh
RUN chmod +x /srv/app/set_ckan_config.sh

# ARG SECRET_KEY
# ENV SECRET_KEY=${SECRET_KEY}

USER ckan
