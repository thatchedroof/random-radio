import json

with open('data/result.json', "r", encoding="utf-8") as f:
    data = json.load(f)

with open('data/date_output.json', "r", encoding="utf-8") as f:
    dates = json.load(f)

with open('data/song_titles_output.json', "r", encoding="utf-8") as f:
    song_titles = json.load(f)

with open('data/html_output.json', "r", encoding="utf-8") as f:
    html_output = json.load(f)

result = {}

for i, (key, value) in enumerate(html_output.items()):
    result[key] = value
    if dates[i]:
        result[key]['date'] = dates[i]
    if song_titles[i]:
        result[key]['song_titles'] = song_titles[i]

with open('data/html_dates_song_tiles.json', "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

# Print the results without a corresponding date in the data
for i, (key, value) in enumerate(result.items()):
    date = value.get('date')
    if not date:
        continue

    found = None
    for entry in data:
        date_str = entry['date']
        if date_str:
            [year, month, day] = date_str.split('-')
            # print(year, month, day)
            if date['year'] == int(year) and date['month'] == int(month) and date['day'] == int(day):
                found = entry
                break

    if not found:
        # print(f"No match found for {date}")
        pass

# Sort the data by date
data.sort(key=lambda x: x['date'])

# Deduplicate the data
def deduplicate_list_of_dicts(lst):
    seen = set()
    unique_list = []
    for d in lst:
        dict_tuple = tuple(d.items())
        if dict_tuple not in seen:
            seen.add(dict_tuple)
            unique_list.append(d)
    return unique_list

print(len(data))
data = deduplicate_list_of_dicts(data)
print(len(data))

def cmp_dates(date1, date2):
    return int(date1['year']) == int(date2['year']) and int(date1['month']) == int(date2['month']) and int(date1['day']) == int(date2['day'])

not_found = 0

# Print the data without a corresponding date in the results
for index, entry in enumerate(data):
    date_str = entry['date']

    if not date_str:
        continue

    [year, month, day] = date_str.split('-')

    data_date = {
        'year': int(year),
        'month': int(month),
        'day': int(day)
    }

    found = None
    for i, (key, value) in enumerate(result.items()):
        [year_2, month_2, day_2, *rest] = key.split("/")

        date_2 = {
            'year': int(year_2),
            'month': int(month_2),
            'day': int(day_2)
        }

        date = value.get('date')

        if not date:
            continue

        # if cmp_dates(date, data_date):
        # if cmp_dates(date_2, data_date):
        if cmp_dates(date, data_date):
            found = value
            # print(f"Match found for {date_str}, {entry['name']}")
            break

    if not found:
        not_found += 1
        print(f"{not_found}: No match found for {date_str}, {entry['name']}")
    else:
        print(json.dumps(data[index], indent=4))
        print(json.dumps(found, indent=4))
        del found['content']
        data[index]['page'] = found

with open('data/data_with_page.json', "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
