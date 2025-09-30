import argparse
import json
from ckan_auto_harvester import CkanAutoHarvester

ckan = CkanAutoHarvester()

def create_org(args):
    resp = ckan.create_org(args.name, args.title, args.description)
    print(json.dumps(resp, indent=2))

def create_harvest(args):
    resp = ckan.create_harvest_source(args.name, args.url, args.owner_org, args.source_type, args.frequency, args.title, args.notes)
    print(json.dumps(resp, indent=2))

def trigger_harvest(args):
    resp = ckan.trigger_harvest(args.source)
    print(json.dumps(resp, indent=2))
    
def federated_harvest(args):
    resp = ckan.federated_harvest(args.sources_file)
    print(json.dumps(resp, indent=2))
    
def update_dataset(args):
    update_flag=False
    if args.json_file:
        with open(args.json_file, "r", encoding="utf-8") as fp:
            resp = ckan.update_dataset(args.id, json.load(fp))
            print(json.dumps(resp, indent=2))
            update_flag=True
    if args.json_data:
        resp = ckan.update_dataset(args.id, args.json_data)
        print(json.dumps(resp, indent=2))
        update_flag=True
    if not update_flag:
        print("Make sure you have provided either json-data or file-path containing json-data for 'updates'")

def upload_data_file(args):
    resp = ckan.upload_file_to_dataset(args.dataset, args.file, args.title)
    print(json.dumps(resp, indent=2))

def link_resource(args):
    resp = ckan.link_resource_to_dataset(args.dataset, args.url, args.title, args.format)
    print(json.dumps(resp, indent=2))
    
# ======================================

def add_sparql(args):
    resp = ckan.add_sparql_endpoint(args.dataset, args.endpoint)
    print(json.dumps(resp, indent=2))

def federated_query(args):
    query = open(args.query_file).read()
    results = ckan.federated_query(args.keyword, query)
    print(json.dumps(results, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Unified CKAN-DCAT CLI tool"
    )
    subparsers = parser.add_subparsers(dest="command")

    # --------------------------
    # ORG
    # --------------------------
    p_org = subparsers.add_parser("create-org", help="Create a CKAN organization")
    p_org.add_argument("--name", required=True)
    p_org.add_argument("--title")
    p_org.add_argument("--description")
    p_org.set_defaults(func=create_org)

    # --------------------------
    # HARVEST
    # --------------------------
    p_harvest = subparsers.add_parser("create-harvest", help="Create a harvest source")
    p_harvest.add_argument("--name", required=True)
    p_harvest.add_argument("--url", required=True)
    p_harvest.add_argument("--owner-org", required=True)
    p_harvest.add_argument("--source-type", default="dcat")
    p_harvest.add_argument("--frequency", default="MANUAL")
    p_harvest.add_argument("--title")
    p_harvest.add_argument("--notes")
    p_harvest.set_defaults(func=create_harvest)

    p_trigger = subparsers.add_parser("trigger-harvest", help="Trigger and monitor a harvest")
    p_trigger.add_argument("--source", required=True, help="Harvest source ID or name")
    p_trigger.set_defaults(func=trigger_harvest)

    # --------------------------
    # FEDERATED HARVEST
    # --------------------------
    p_fed = subparsers.add_parser("federated-harvest", help="Run federated harvesting from multiple sources")
    p_fed.add_argument("--sources-file", required=True, help="Path to JSON file with federated sources")
    p_fed.set_defaults(func=federated_harvest)
    
    # --------------------------
    # DATASETS
    # --------------------------
    p_update = subparsers.add_parser("update-dataset", help="Update dataset metadata")
    p_update.add_argument("--id", required=True)
    p_update.add_argument("--json-data", help="JSON string of fields to update")
    p_update.add_argument("--json-file", help="File containing JSON string of fields to update")
    p_update.set_defaults(func=update_dataset)

    p_upload = subparsers.add_parser("upload-data-file", help="Upload local file as dataset resource")
    p_upload.add_argument("--dataset", required=True)
    p_upload.add_argument("--title", required=True)
    p_upload.add_argument("--file", required=True)
    p_upload.set_defaults(func=upload_data_file)

    p_link = subparsers.add_parser("link-resource", help="Link an external resource to dataset")
    p_link.add_argument("--dataset", required=True)
    p_link.add_argument("--title", required=True)
    p_link.add_argument("--url", required=True)
    p_link.add_argument("--format", default="CSV")
    p_link.set_defaults(func=link_resource)

    # --------------------------
    # SPARQL
    # --------------------------
    p_sparql = subparsers.add_parser("add-sparql", help="Add SPARQL endpoint to dataset metadata")
    p_sparql.add_argument("--dataset", required=True)
    p_sparql.add_argument("--endpoint", required=True)
    p_sparql.set_defaults(func=add_sparql)

    p_federated = subparsers.add_parser("federated-query", help="Run federated query across datasets")
    p_federated.add_argument("--keyword", required=True, help="Search keyword (e.g., Flood)")
    p_federated.add_argument("--query-file", required=True, help="SPARQL query file")
    p_federated.set_defaults(func=federated_query)

    # --------------------------
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
