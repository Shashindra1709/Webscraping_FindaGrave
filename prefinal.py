import time
import sys
import re  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


sys.stdout.reconfigure(encoding='utf-8')


first_name = "andrews"
last_name = ""
url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&lastname={last_name}&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1#sr-170512167"


driver = webdriver.Chrome() 
driver.get(url)
  
time.sleep(10)

all_data = []

previous_result_count = 0

while True:
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    #remove unwanted tags
    for unwanted_tag in soup.find_all(['span', 'small', 'figure']):  
        if ('icon-findagrave' in unwanted_tag.get('class', []) or
            'icon-flowers' in unwanted_tag.get('class', []) or
            'text-muted' in unwanted_tag.get('class', []) or
            unwanted_tag.get('aria-label') in ['No grave photo', 'Flowers have been left.'] or
            'visually-hidden' in unwanted_tag.get('class', [])):
            #print(f"Removing tag: {unwanted_tag}")
            unwanted_tag.decompose()


    name_tags = soup.find_all('h2', class_='name-grave')
    date_tags = soup.find_all('b', class_='birthDeathDates')

    names = []
    birth_dates = []
    death_dates = []

    # Extract names
    for tag in name_tags:
        raw_name = tag.get_text(separator=" ", strip=True)

        # Clean up the name
        clean_name = re.sub(r'[“”]', '', raw_name) 
        clean_name = re.sub(r'[^\w\s,.]', '', clean_name)  
        clean_name = re.sub(r'\s{2,}', ' ', clean_name).strip()  

        names.append(clean_name)

    # Extract birth and death dates
    for tag in date_tags:
        date_text = tag.get_text(strip=True)


        if date_text == "Birth and death dates unknown.":
            birth_dates.append(None)
            death_dates.append(None)
        else:
            birth_date, death_date = [d.strip() for d in date_text.split('–')]
            birth_dates.append(birth_date)
            death_dates.append(death_date)


    page_data = list(zip(names, birth_dates, death_dates))

    # Add unique entries
    for entry in page_data:
        if entry not in all_data:
            all_data.append(entry)

    if len(all_data) == previous_result_count:
        print("No more content loaded. Stopping.")
        break

    previous_result_count = len(all_data)

    # scrolling to load content gradually
    for _ in range(10): 
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

    time.sleep(2)

print(f"Total entries extracted: {len(all_data)}")
for name, birth_date, death_date in all_data:
    if birth_date and death_date:
        print(f"Name: {name}, Birth Date: {birth_date}, Death Date: {death_date}")
    else:
        print(f"Name: {name}, Birth Date: Unknown, Death Date: Unknown")


# print(f"Total entries extracted: {len(all_data)}")

# df = pd.DataFrame(all_data, columns=["Name", "Birth Date", "Death Date"])

# print(df)

# df.to_csv('C:/Users/USER/Desktop/Output_Grave/findagrave_data1.csv', index=False)

driver.quit()
