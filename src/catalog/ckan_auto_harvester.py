import requests
import urllib3
import time
import json
from config import API_KEY, CKAN_URL, VERIFY_SSL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CkanAutoHarvester:
    def __init__(self, api_key=API_KEY, base_url=CKAN_URL, verify_ssl=VERIFY_SSL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def _post(self, action, payload):
        url = f"{self.base_url}/api/3/action/{action}"
        resp = requests.post(url, json=payload, headers=self.headers, verify=self.verify_ssl)
        return resp.json()

    def _get(self, action, params):
        url = f"{self.base_url}/api/3/action/{action}"
        resp = requests.get(url, params=params, headers=self.headers, verify=self.verify_ssl)
        return resp.json()

    # -------------------------
    # ORG METHODS
    # -------------------------
    def create_org(self, name, title=None, description=None):
        payload = {"name": name}
        if title:
            payload["title"] = title
        if description:
            payload["description"] = description
        return self._post("organization_create", payload)

    # -------------------------
    # HARVEST METHODS
    # -------------------------
    def create_harvest_source(self, name, url, owner_org, source_type="dcat",frequency="MANUAL", title=None, notes=None):
        payload = {
            "name": name,
            "url": url,
            "source_type": source_type,
            "frequency": frequency,
            "owner_org":owner_org
        }
        if title:
            payload["title"] = title
        if notes:
            payload["notes"] = notes
        return self._post("harvest_source_create", payload)

    def resolve_source_id(self, source_identifier):
        """Resolve a harvest source name or UUID into a UUID."""
        params = {"id": source_identifier}
        resp = self._get("harvest_source_show", params)

        if not resp.get("success"):
            raise ValueError(f"Could not resolve harvest source: {source_identifier} → {resp}")

        result = resp.get("result")
        if not result or "id" not in result:
            raise ValueError(f"No valid source found for {source_identifier}")

        return result["id"]  # Always UUID
    def trigger_harvest(self, source_id):
        try:
            source_uuid = self.resolve_source_id(source_id)
            print("Resolved UUID:", source_uuid)
            payload = {"source_id": source_uuid}
            resp = self._post("harvest_job_create", payload)
            return resp
        except Exception as e:
            print("Error triggering harvest:", str(e))
            return {"success": False, "error": str(e)}
    
    def get_last_harvest_job(self, source_id):
        resp = self._get("harvest_source_show", {"source_id": source_id})
        if not resp.get("success"):
            return None
        jobs = resp["result"].get("status", {}).get("last_jobs", [])
        return jobs[0] if jobs else None


    
    def wait_for_harvest_completion(self, source_identifier, poll_interval=10):
        source_uuid = self.resolve_source_id(source_identifier)
        print(f"Polling harvest job status for source: {source_identifier} ...")
        while True:
            job = self.get_last_harvest_job(source_uuid)
            if not job:
                print("No job found yet. Waiting...")
            else:
                state = job.get("status")
                print(f"Current harvest job state: {state}")
                if state in ["Finished", "Completed", "Failed", "Errored"]:
                    print(f"Harvest finished with status: {state}")
                    break
            time.sleep(poll_interval)


    def federated_harvest(self, sources_file: str):
        """Harvest datasets from multiple federated sources"""
        with open(sources_file, "r") as f:
            sources = json.load(f)

        results = []
        for src in sources:
            # create_harvest_source(self, name, url, owner_org, source_type="dcat",frequency="MANUAL", title=None, notes=None)
            print(f" Harvesting from {src['name']} ({src['url']}) ...")
            resp = self.create_harvest_source(
                src["name"], src["url"], src["owner_org"],
                source_type=src.get("source_type", "dcat"),
                frequency=src.get("frequency", "MANUAL"),
                title=src.get("title"),
                notes=src.get("notes")
            )
            results.append(resp)

        return results
    # -------------------------
    # DATASET METHODS
    # -------------------------

    def update_dataset(self, dataset_id, updates: dict):
        updates["id"] = dataset_id
        return self._post("package_update", updates)

    def upload_file_to_dataset(self, dataset_id, file_path):
        url = f"{self.base_url}/api/3/action/resource_create"
        with open(file_path, "rb") as fp:
            files = {"upload": fp}
            data = {"package_id": dataset_id}
            resp = requests.post(
                url, headers={"Authorization": self.api_key},
                data=data, files=files, verify=self.verify_ssl
            )
        return resp.json()

    def link_resource_to_dataset(self, dataset_id, resource_url, format="CSV"):
        payload = {
            "package_id": dataset_id,
            "url": resource_url,
            "format": format
        }
        return self._post("resource_create", payload)

    # -------------------------
    # SPARQL EXTENSIONS
    # -------------------------
    def add_sparql_endpoint(self, dataset_id, sparql_url):
        """
        Attach SPARQL endpoint metadata to a dataset (DCAT-style).
        """
        extra = {"key": "dcat:accessURL", "value": sparql_url}
        payload = {"id": dataset_id, "extras": [extra]}
        return self._post("package_update", payload)

    def search_datasets(self, keyword):
        """
        Search CKAN datasets by keyword.
        """
        resp = self._get("package_search", {"q": keyword})
        if not resp.get("success"):
            return []
        return resp["result"]["results"]

    def get_sparql_endpoints(self, keyword):
        """
        Return list of SPARQL endpoints from datasets matching keyword.
        """
        datasets = self.search_datasets(keyword)
        endpoints = []
        for ds in datasets:
            extras = ds.get("extras", [])
            for e in extras:
                if e["key"].lower() in ["dcat:accessurl", "sparql_endpoint"]:
                    endpoints.append(e["value"])
        return endpoints

    def run_sparql_query(self, endpoint_url, query):
        """
        Execute a SPARQL query against a given endpoint.
        """
        headers = {"Accept": "application/sparql-results+json"}
        resp = requests.get(endpoint_url, params={"query": query}, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}

    def federated_query(self, keyword, query_template):
        """
        Run the same SPARQL query against all endpoints discovered by keyword.
        """
        endpoints = self.get_sparql_endpoints(keyword)
        results = {}
        for ep in endpoints:
            print(f"Querying {ep}...")
            results[ep] = self.run_sparql_query(ep, query_template)
        return results
