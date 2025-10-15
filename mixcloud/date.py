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

dates = []

class DateResponse(BaseModel):
    year: int
    month: int
    day: int

class NoDate(BaseModel):
    message: str

class Response(BaseModel):
    date: DateResponse | NoDate

for key, value in tqdm.tqdm(html_output.items()):
    soup = BeautifulSoup(value['content'], 'lxml')

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extract the date from this entry: {value['title']}. If there is no date, return 'No date found'."}],
        response_format=Response
    )

    date = json.loads(completion.choices[0].message.content)['date']
    if 'year' in date:
        dates.append(date)
    else:
        dates.append(None)

    print(completion.choices[0].message.content)

    print('TITLE:', value['title'])
    # print(md(value['content']))

    break

with open('date_output.json', 'w', encoding="utf-8") as f:
    json.dump(dates, f, indent=4)
