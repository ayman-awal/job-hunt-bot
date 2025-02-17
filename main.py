import os
from dotenv import load_dotenv # type: ignore
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import re

load_dotenv()

google_search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
cse_id = os.getenv("CSE_ID")
sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
from_email = os.getenv("FROM_EMAIL")
to_email = os.getenv("TO_EMAIL")


query = 'Software Engineer "USA" OR "United States" site:boards.greenhouse.io'
keywords = ["entry level", "junior", "level I", "software engineer"]

jobData = []
for start in range(1, 101, 10): 
    print("here")
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_search_api_key}&cx={cse_id}&start={start}"
    response = requests.get(url)
    print(response)
    data = response.json()
    print(data)
    
    if 'items' in data:
        jobData.extend(data['items'])
    else:
        break


filteredJobs = []

for data in jobData:
    try:
        response = requests.get(data, headers={"User-Agent": "Mozilla/5.0"})
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


def sendEmail():
    content = ""

    with open("filtered_jobs.txt", "r") as f:
        content = f.read() 
        print(content) 

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject='Trial',
        html_content=content)
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)