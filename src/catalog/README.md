
# CKAN Harvest Automation

This project automates the management of CKAN datasets and DCAT harvest sources. Using ckanctl.py, you can register datasets, harvest metadata from external catalogs, upload sample data, and perform federated SPARQL queries.

This project provides scripts to automate a number of features.

## Features
- Create CKAN organizations: Define the owner organisation of datasets and harvest sources.
- Register DCAT harvest sources: Connect external DCAT-compliant catalogs for metadata harvesting.
- Trigger and monitor harvesting jobs: Start harvest jobs and track their progress.
- Update dataset metadata: Change titles, descriptions, tags, etc.
- Upload sample datasets: Add CSV/JSON data from file or network for testing or demonstration.
- Attach SPARQL endpoints: Link datasets to SPARQL services for query federation.
- Run federated SPARQL queries: Search multiple catalogs simultaneously.
- Modular Python classes: Scripts are reusable and can be integrated into custom workflows.
- Configurable API key and CKAN URL: Easy setup via `config.py`.

---

## Configuration
Before running commands, configure your CKAN instance in config.py:
```python
API_KEY = "your-ckan-api-key"
CKAN_URL = "https://localhost:8443/api/3/action"
VERIFY_SSL = False   # Set True if using valid SSL certificates
```
Note:
- API_KEY → You can generate as stated above [under your CKAN user profile (/user/me)]
- CKAN_URL → Public URL of your CKAN portal (with nginx/SSL)
- VERIFY_SSL → False if you are using self-signed certs


## Generate API_KEY
To use CKAN API, we need API_KEY ready in hand. We can generate API_KEY from CKAN portal through the following steps:

1. login to the CKAN portal (default admin user: ckan_admin and password:test1234). 
2. click on the user profile showed around the top-right corner
3. click on the (4th) tab API Tokens
4. name the token and click on the "Create API Token" button
It will show an API_KEY on above the form. This data will not be saved in the CKAN system. So, you must save it somewhere for further reference.

---

# ckanctl – CKAN-DCAT Management CLI

`ckanctl` is a unified Python-based command-line interface (CLI) tool to manage CKAN-DCAT operations programmatically.  
It allows you to create organizations, register harvest sources, trigger harvesting, upload datasets, and update metadata from the command line.

---

## Usage
The CLI is powered by argparse. We can see all avaialble commands:
```bash
python ckanctl.py -h
python ckanctl.py --help
```

The general structure of the CLI tool using Python:

```bash
python ckanctl.py <command> [--arg_1 value_1 --arg_2 value_2 ... --arg_n value_n]
```

### Organisation Management

#### Create Organization
```bash
python ckanctl.py create-org --name <name> --title <title> --description <description>
```
Note:
- --name → unique identifier or name specified in lower case and alpha-numeric characters only for an organisation
- --title → human-readable title of the organisation

Example:
```bash
python ckanctl.py create-org --name flood-org --title "Flood Research" --description "Organization for flood-related datasets"
```

### Harvesting Management

#### Create Harvest Source
Register a Harvest source:
```bash
python ckanctl.py create-harvest --name <name> --url <url> --source-type <source-type> --owner-org <organization> [--title <title> --frequency <frequency> --notes <notes>]
```
Note:
- --name → unique identifier of the harvesting source
- --title → source title
- --url → DCAT endpoint URL, which may often contain CONSTRUCT query to ensure rdf metadata
- --type → type of harvester (e.g. dcat_rdf)
- --org → owning organization

Example:

```bash
python ckanctl.py create-harvest --name credo-harvest --url "https://credo.theworldavatar.io/power/blazegraph/ui/namespace/kb/sparql?query=CONSTRUCT%20%7B%3Fs%20%3Fp%20%3Fo%7D%20WHERE%20%7B%3Fs%20%3Fp%20%3Fo%7D&format=" --source-type dcat_rdf --owner-org flood-org
```
CKAN-DCAT harvesters (like dcat_rdf) are designed to extract dataset metadata, not raw data triples. Collecting all raw data may sometimes raise error "Remote file is too big."
To handle this type of error, we can simply collect all sort of metadata only, rather than collecting all data triples.

```SPARQL
PREFIX dcat: <http://www.w3.org/ns/dcat#>

CONSTRUCT {
  ?dataset ?p ?o .
}
WHERE {
  ?dataset a dcat:Dataset ;
           ?p ?o .
}
```
This SPARQL produces datasets and relevant properties: 
- ?dataset a dcat:Dataset ensures we only fetch resources that are datasets.
- ?p ?o retrieves all properties for that dataset, not just title/description.
- We can also LIMIT 100 (which is optional) that can eliminate chances to avoid huge payloads.

Example:

```bash
https://pirmasens.cmpg.io/blazegraph/namespace/cea/sparql?query=CONSTRUCT%20%7B%3Fdataset%20%3Fp%20%3Fo%7D%20WHERE%20%7B%3Fdataset%20a%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fdcat%23Dataset%3E%20%3B%20%3Fp%20%3Fo%20.%7D&format=text/turtle
```
#### Trigger Harvest

```bash
python ckanctl.py trigger-harvest --source <source_id>
```

Example:
```bash
python ckanctl.py trigger-harvest --source 5224bea4-79e4-4fb6-bd9c-4b0ee70dfdad
```

### Dataset Management

#### Update dataset

```bash
python ckanctl.py update_dataset --id <dataset_id> [--json-data <json_formated_data> --json-file <file_path>]
```
Note: You may provide either json formatted metadata or a file_path where there is a json formatted metadata about a dataset. If you provide both of them, it will first change dataset with the filed json data, and json_formatted direct data will update the datasets later. This means, if there is a overlap on metadata, direct json-formatted metadata will persist.

Providing only id will not modify any metadata
Example:
```bash
python ckanctl.py update_dataset --id 5234bea4-79e4-4fb6-bd9c-4b0ee70dfdad
```

#### Load Sample Dataset from File
Use this command when you have a CSV, JSON, or other compatible file on your computer that you want to load and associate into a CKAN dataset. This can be a sample dataset that may help to validate any service before running against real data.

```bash
python ckanctl.py upload-data-file --dataset <dataset_name> --file <file_path>
```

Example:
```bash
python ckanctl.py upload-data-file --dataset credo-harvest --file "data/climate_data.csv"
```

#### Load Sample Dataset from External Link
Use this when your sample data is hosted online, such as on a public URL. The tool will fetch the file and load it into the dataset.
```bash
python ckanctl.py link-resource --dataset credo-harvest --url "data/climate_data.csv" --format "csv"
```
Example:
```bash
python ckanctl.py link-resource --dataset credo-harvest --url "data/climate_data.csv"
```

#### Add SPARQL Endpoint to Dataset
Use this when your dataset is associated with a SPARQL endpoint. 
```bash
python ckanctl.py add-sparql --dataset credo-harvest --endpoint "https://kaiserslautern.cmpg.io/blazegraph/namespace/cea/sparql"
```

#### Add SPARQL Endpoint to Dataset
Use this when your want to search datasets with keywords and federate a SPARQL written in a file against all endpoints to produce consolidated output. 
```bash
python ckanctl.py federated-query --keyword credo-harvest --query-file "query/sparql.txt"
```



## Configuration Notes

- **API Key**: Must be from a CKAN sysadmin user.
- **Organization Ownership**: Harvest sources and datasets must belong to an existing organization.
- **SSL Verification**: Disable for local/self-signed certs.

---

## License

