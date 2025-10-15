import json
from bs4 import BeautifulSoup
import tqdm
from markdownify import markdownify as md
import dotenv
from openai import OpenAI
from pydantic import BaseModel

dotenv.load_dotenv()

client = OpenAI()

with open('html_output.json', 'r', encoding="utf-8") as f:
    html_output = json.load(f)

with open('result.json', "r", encoding="utf-8") as f:
    data = json.load(f)

with open('date_output.json', "r", encoding="utf-8") as f:
    dates = json.load(f)

with open('song_titles_output.json', "r", encoding="utf-8") as f:
    results = json.load(f)

class Song(BaseModel):
    artist: str
    title: str
    link: str

class Response(BaseModel):
    songs: list[Song]

for i, (key, value) in enumerate(tqdm.tqdm(html_output.items())):
    if i < len(results):
        continue

    date = dates[i]

    if not date:
        results.append(None)
        continue

    soup = BeautifulSoup(value['content'], 'lxml')

    content = md(value['content'])

    # print(content)

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extract the artists, titles, and links from the following entry. If a title or link is missing, leave it as an empty string. Ignore other content, such as the record label.\n\n{content}"}],
        response_format=Response
    )

    songs = json.loads(completion.choices[0].message.content)['songs']
    results.append(songs)

    # print(songs)

    # print(md(value['content']))

    with open('song_titles_output.json', 'w', encoding="utf-8") as f:
        json.dump(results, f, indent=4)

