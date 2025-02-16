import os
from dotenv import load_dotenv # type: ignore
import requests # type: ignore
from bs4 import BeautifulSoup
import re

load_dotenv()

api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
cse_id = os.getenv("CSE_ID")


query = 'Software Engineer "USA" OR "United States" site:boards.greenhouse.io'
keywords = ["entry level", "junior", "level I", "software engineer"]

jobData = []
for start in range(1, 101, 10): 
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&start={start}"
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data:
        jobData.extend(data['items'])
    else:
        break


filteredJobs = []

for data in jobData:
    # print(data['link'])
    # print(data['title'])
    # print("\n")
    try:
        response = requests.get(data['link'], headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, "html.parser")

        page_text = soup.get_text(separator=" ").lower()

        if any(re.search(rf"\b{k.lower()}\b", page_text) for k in keywords):
            print("adding job")
            filteredJobs.append({"title": data['title'], "url": data['link']})

    except Exception as e:
        print(f"Error processing {url}: {e}")

with open("filtered_jobs.txt", "w") as f:
    for job in filteredJobs:
        f.write(job['title'] + "\n" + job['url'] + "\n")

