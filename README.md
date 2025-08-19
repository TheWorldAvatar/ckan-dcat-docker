# Spin up CKAN docker-compose.yml
## Base mode

Use this if you are a maintainer and will not be making code changes to CKAN or to CKAN extensions

Modify `.env` depending on your own needs.

> [!WARNING]
> There is a sysadmin user created by default with the values defined in `CKAN_SYSADMIN_NAME` and `CKAN_SYSADMIN_PASSWORD` (`ckan_admin` and `test1234` by default). These must be changed before running this setup as a public CKAN instance.

To build the images:

```bash
	docker compose build
```

To start the containers:

```bash
	docker compose up
```

This will start up the containers in the current window. By default the containers will log direct to this window with each container
using a different colour. You could also use the -d "detach mode" option ie: `docker compose up -d` if you wished to use the current
window for something else.

After this step, CKAN should be running at `CKAN_SITE_URL` (by default https://localhost:8443) at the port of nginx

This repo provides a custom Dockerfile with DCAT extension and Harvester.

# Test harvesting the metadata from the CReDO Blazegraph repo
I tested harvesting the metadata from the CReDo Blazegraph repository with the URL: https://credo.theworldavatar.io/power/blazegraph/ui/namespace/kb/sparql?query=CONSTRUCT%20%7B%3Fs%20%3Fp%20%3Fo%7D%20WHERE%20%7B%3Fs%20%3Fp%20%3Fo%7D&format=

## Steps to Test Harvesting
Step-1: Login to the CKAN site (https://localhost:8443) with user-name and password (`ckan_admin` and `test1234` by default)
Step-2: Create an organization (https://localhost:8443/dashboard/organizations)
Step-3: Go to the url https://localhost:8443/harvest and click "Add Harvest Source"
Step-4: Create a harvest source
Step-5: Click "Admin" and then "Reharvest" tab
Step-6: Wait/refresh till it collects all datasets from the repository 

<!-- # Document differences between our current use of DCAT/DCTerms predicates and CKAN/DCAT-AP's use
# Try adding the CKAN, datapusher and solr services to the stack
# Intergrate the new services with the existing services (postgres, dragonfly (redis))
# Added code to data uploader to perform harvesting when data uploaded -->
