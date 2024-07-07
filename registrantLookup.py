import requests
import json
import argparse

def get_domains(api, rn, d="2020-01-01", m="preview"):
    url = "https://registrant-alert.whoisxmlapi.com/api/v2"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "apiKey": api,
        "sinceDate": d,
        "mode": m,
        "advancedSearchTerms": [{
            "field": "RegistrantContact.Organization",
            "term": rn
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        if m == "preview":
            domains_count = data.get('domainsCount', 0)
            return domains_count
        else:
            domains = data.get('domainsList', [])
            return domains
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get domains by registrant name")
    parser.add_argument("-api", required=True, help="API key for authentication")
    parser.add_argument("-rn", required=True, help="Registrant name to search for")
    parser.add_argument("-d", default="2020-01-01", help="Start date for the search in YYYY-MM-DD format")
    parser.add_argument("-m", default="preview", help="Mode for the API request (default is 'preview')")

    args = parser.parse_args()

    if not args.api:
        print("Error: An API key must be provided.")
        exit(1)

    if not args.rn:
        print("Error: A registrant name must be provided.")
        exit(1)

    result = get_domains(args.api, args.rn, args.d, args.m)

    if args.m == "purchase":
        if result:
            print(f"Domains owned by {args.rn} found:")
            for domain in result:
                print(domain)
    else:
            print("No domains found or an error occurred.")
    elif args.m == "preview":
        print("Preview search completed, use mode purchase to display domains")
        print(f"Domains owned by {args.rn} found: {result}")
