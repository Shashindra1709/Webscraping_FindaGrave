import time
import sys
import re  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import json



sys.stdout.reconfigure(encoding='utf-8')


first_name = "priya"
last_name = ""
published_year = "2020"
url = f"https://www.legacy.com/api/_frontend/search?endDate=2024-12-06&firstName={first_name}&keyword=&lastName={last_name}&limit=50&noticeType=all&session_id=&startDate={published_year}-01-01"
driver = webdriver.Chrome() 
driver.get(url)

time.sleep(10)


while True:
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #print(soup.text)

    # response = requests.get(url, verify=False)
    # response.raise_for_status()

#     soup = BeautifulSoup(driver.page_source, 'html.parser')

    json_data = json.loads(soup.text)

    #print(json.dumps(json_data, indent=4, ensure_ascii=False))

    with open('obituaries_data.json', 'w') as file:
        json.dump(json_data, file)

    driver.quit()        
    break

with open('obituaries_data.json', 'r') as file:
    data = json.load(file)

# print(json.dumps(data, indent = 2))

orbituaries = data.get('obiuaries', [])

filtered_data = []

def clean_name(name):
    return re.sub(r'\"(.*?)\"', r'\1', name)

for obituary in data['obituaries']:
    full_name = obituary['name']['fullName']
    full_name = clean_name(full_name)
    age = obituary.get('age')
    From_To_Years = obituary.get('fromToYears')
    #location
    location = obituary.get('location', {})
    city = location.get('city', {}).get('fullName', 'Unknown')
    state = location.get('state', {}).get('fullName', 'Unknown')
    full_location = f"{city}, {state}" if city and state else "Unknown"


    filtered_data.append({
        'full_name': full_name,
        'age': age,
        'From_To_Years' : From_To_Years,
        'location': full_location
    })


for entry in filtered_data:
    print(f"Full Name: {entry['full_name']}, Dates : {entry['From_To_Years']}, Age: {entry['age']}, location : {entry['location']}")

print(f"Total maching records :{len(filtered_data)}")






