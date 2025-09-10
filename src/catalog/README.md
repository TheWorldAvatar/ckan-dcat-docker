
# CKAN Harvest Automation

This project provides scripts to automate anumber of features.

## Features
- Create CKAN organizations for defining OWNER_ORG of data
- Register DCAT harvest sources
- Trigger and monitor harvesting jobs
- Upload sample datasets (from file or external link)
- Update dataset metadata fields
- Attach SPARQL endpoints to datasets (Optional)
- Run federated SPARQL queries across harvested catalogs
- Modular design with reusable Python classes
- Configurable API key and CKAN URL via `config.py`

---

## Generate API_KEY
To use CKAN API, we need API_KEY ready in hand. We can generate API_KEY from CKAN portal through the following steps:

1. login to the CKAN portal (default admin user: ckan_admin and password:test1234). 
2. click on the user profile showed around the top-right corner
3. click on the (4th) tab API Tokens
4. name the token and click on the "Create API Token" button
It will show an API_KEY on above the form. This data will not be saved in the CKAN system. So, you must save it somewhere for further reference.

# ckanctl – CKAN-DCAT Management CLI

`ckanctl` is a unified Python-based command-line interface (CLI) tool to manage CKAN-DCAT operations programmatically.  
It allows you to create organizations, register harvest sources, trigger harvesting, upload datasets, and update metadata from the command line.

---

## Configuration
Configure your CKAN connection by editing `config.py`:
   ```python
   # config.py
   CKAN_URL = "https://localhost:8443"
   API_KEY = "your-ckan-api-key"
   VERIFY_SSL = False  # Set True if using a trusted SSL cert
   ```

- API_KEY → You can generate as stated above [under your CKAN user profile (/user/me)]
- CKAN_URL → Public URL of your CKAN portal (with nginx/SSL)
- VERIFY_SSL → False if you are using self-signed certs
---

## Usage
Run:
```bash
python ckanctl.py -h
python ckanctl.py --help
```

The general structure of the CLI tool using Python:

```bash
python ckanctl.py <command> [options]
```

### Organisation Management

#### Create Organization
```bash
python ckanctl.py create-org --name <name> --title <title> --description <description>
```

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

Example:

```bash
python ckanctl.py create-harvest --name credo-harvest --url "https://credo.theworldavatar.io/power/blazegraph/ui/namespace/kb/sparql?query=CONSTRUCT%20%7B%3Fs%20%3Fp%20%3Fo%7D%20WHERE%20%7B%3Fs%20%3Fp%20%3Fo%7D&format=" --source-type dcat_rdf --owner-org flood-org
```

#### Trigger Harvest

```bash
python ckanctl.py trigger-harvest --source <source_id_or_name>
```

Example:
```bash
python ckanctl.py trigger-harvest --source credo-harvest
```

### Dataset Management






















#### Load Sample Dataset from File
```bash
python ckanctl.py load-sample-file <dataset_name> <file_path> [--org <organization>]
```

Example:
```bash
python ckanctl.py trigger-harvest --source credo-harvest
```

#### Load Sample Dataset from External Link
```bash
python ckanctl.py load-sample-link <dataset_name> <url> [--org <organization>]
```
Example:
```bash
python ckanctl.py trigger-harvest --source credo-harvest
```

#### Update Dataset Metadata
```bash
python ckanctl.py update-dataset <dataset_name> --field key=value [--field key=value ...]
```

Example:
```bash
python ckanctl.py trigger-harvest --source credo-harvest
```

---

## Configuration Notes

- **API Key**: Must be from a CKAN sysadmin user.
- **Organization Ownership**: Harvest sources and datasets must belong to an existing organization.
- **SSL Verification**: Disable for local/self-signed certs.

---

## License

