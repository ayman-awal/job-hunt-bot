import os
from dotenv import load_dotenv # type: ignore
import requests # type: ignore

load_dotenv()

api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
cse_id = os.getenv("CSE_ID")


query = 'Software Engineer "USA" OR "United States" site:boards.greenhouse.io'

results = []
for start in range(1, 101, 10): 
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&start={start}"
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data:
        results.extend(data['items'])
    else:
        break

print(len(results))
for item in results:
    # print(f"Title: {item['title']}")
    # print(f"URL: {item['link']}")
    print(item)