import os
import json
import sys
from bs4 import BeautifulSoup
import tqdm
from lxml import etree

path = ".\download\Other Rock Show\otherrockshow.wordpress.com"

def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html5lib')

    if not soup:
        print(f"Error: Could not parse \"{file_path}\"")

    for tag in soup.find_all("h1"):
        print(tag)

    for tag in soup(["script", "style"]):
        tag.decompose()

    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    try:
        title = soup.find("h1", class_="entry-title").text
    except Exception as e:
        print(f"Error: {e} for \"{file_path}\"")
        title = ""
    # date = soup.find("time", class_="entry-date")["datetime"]
    content = str(soup.find("div", class_="entry-content"))

    return {
        "title": title,
        "content": content,
    }

paths = []

# Years
for year in os.listdir(path):
    year_path = os.path.join(path, year)
    if not os.path.isdir(year_path):
        continue

    try:
        int(year)
    except ValueError:
        continue

    # Months
    for month in os.listdir(year_path):
        month_path = os.path.join(year_path, month)

        if not os.path.isdir(month_path):
            print('continue', month_path)
            continue

        # Days
        for day in os.listdir(month_path):
            folder_path = os.path.join(month_path, day)
            if not os.path.isdir(folder_path):
                continue

            # Entries
            for entry in os.listdir(folder_path):
                entry_path = os.path.join(folder_path, entry)
                if not os.path.isdir(entry_path):
                    continue

                key = f"{year}/{month}/{day}/{entry}"
                paths.append([key, entry_path])

out_path = 'html_output.json'
with open('html_output copy.json', "r", encoding="utf-8") as f:
    out = json.load(f)

for [key, entry_path] in (pbar := tqdm.tqdm(paths)):
    if key in out:
        continue

    year, month, day, entry = key.split("/")
    pbar.set_description(f"{year}/{month}/{day}")

    # Process HTML file
    file_path = os.path.join(entry_path, "index.html")

    try:
        data = process_html_file(file_path)
    except Exception as e:
        print(f"Error: {e} for \"{key}\"")
        continue

    data["path"] = entry_path

    out[key] = data

    with open(out_path, "w", encoding="utf-8") as out_file:
        json.dump(out, out_file, indent=4)

    # print(data)
