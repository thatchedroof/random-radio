import requests
import time
import json
from itertools import cycle
import sys
import csv
import random
import dateparser
from tqdm import tqdm
import re

def fetch_mixcloud_data(query="other rock", delay=1, output_file="mixcloud_results.json"):
    base_url = "https://api.mixcloud.com/search/"
    params = {"q": query, "type": "cloudcast"}
    results = []
    next_url = base_url
    spinner = cycle(['-', '\\', '|', '/'])

    while next_url:
        sys.stdout.write(f"\rFetching data {next(spinner)}")
        sys.stdout.flush()

        response = requests.get(next_url, params=params if next_url == base_url else None)

        if response.status_code != 200:
            print(f"\nError {response.status_code}: {response.text}")
            break

        data = response.json()
        results.extend(data.get("data", []))
        next_url = data.get("paging", {}).get("next")

        # Save results to JSON file
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)

        if next_url:
            time.sleep(delay)  # Avoid hitting the rate limit

    sys.stdout.write("\rFetching complete!      \n")
    return results

if __name__ == "__main__":
    with open("mixcloud_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open("date_names.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        names = [row for row in reader]

    dates = [dateparser.parse(date[2]) for date in names if date[2]]

    # Print the dates per year
    dates_per_year = {}
    for date in dates:
        year = date.year
        dates_per_year[year] = dates_per_year.get(year, 0) + 1

    for year, count in dates_per_year.items():
        print(f"{year}: {count}")

    result = []

    for [slug, name, date] in names:
        obj = {
            "name": name,
            "date": date,
            "slug": slug,
        }

        # Find the matching data from Mixcloud
        for item in data:
            if re.search(slug, item["slug"], re.IGNORECASE):
                obj["key"] = item["key"]
                obj["audio_length"] = item["audio_length"]
                break

        # If no match was found, print the slug
        if "audio_length" not in obj:
            print(f"No match found for {slug}")

        result.append(obj)

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
