"""
import time
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

# Setup URL
first_name = "andrews"
last_name = ""
url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&{last_name}=&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1#sr-170512167"

driver = webdriver.Chrome()  # Ensure you have the correct version of ChromeDriver
driver.get(url)

time.sleep(3)

all_data = []

previous_result_count = 0

while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract names
    name_tags = soup.select('h2.name-grave i')
    names = [tag.get_text(strip=True) for tag in name_tags]

    # Extract birth and death dates
    date_tags = soup.select('b.birthDeathDates')
    dates = [
        tuple(tag.get_text(strip=True).split('–'))  # Split into (birth, death)
        for tag in date_tags
    ]

    page_data = list(zip(names, dates))

    # Add unique entries
    for entry in page_data:
        if entry not in all_data:
            all_data.append(entry)

    # Check
    if len(all_data) == previous_result_count:
        print("No more content loaded. Stopping.")
        break

    previous_result_count = len(all_data)

    # Incremental scroll
    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1) 

    time.sleep(2)  

# Print the results
print(f"Total entries extracted: {len(all_data)}")
for name, (birth, death) in all_data:
    print(f"Name: {name}, Birth Date: {birth.strip()}, Death Date: {death.strip()}")

# Close the driver
driver.quit()




#########################


import time
import sys
import re  # Importing the regular expression module
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Fix encoding
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

    # Extract names
    names = []
    name_tags  = soup.find('h2', class_='name-grave')
    for tag in name_tags:
        # Flatten all text within the `h2` tag into a single string
        raw_name = tag.get_text(separator=" ", strip=True)
        
        # Clean up the name
        clean_name = re.sub(r'[“”]', '', raw_name)  
        clean_name = re.sub(r'[^\w\s,.]', '', clean_name)  
        clean_name = re.sub(r'\s{2,}', ' ', clean_name).strip()  
        
        names.append(clean_name)

    # Extract birth and death dates
    date_tags = soup.find('b', class_='birthDeathDates')
    dates = []

    for tag in date_tags:
        date_text = tag.get_text(strip=True)
        # Handle "unknown" dates case
        if date_text == "Birth and death dates unknown.":
            dates.append((None, None))  # No dates available
        else:
            # Split dates and remove excess spaces
            birth_date, death_date = [d.strip() for d in date_text.split('–')]
            dates.append((birth_date, death_date))

    # Combine
    page_data = list(zip(names, dates))

    #unique entries
    for entry in page_data:
        if entry not in all_data:
            all_data.append(entry)

    # Check
    if len(all_data) == previous_result_count:
        print("No more content loaded. Stopping.")
        break 

    previous_result_count = len(all_data)

    # Incremental scrolling to load content gradually
    for _ in range(10): 
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)  

    time.sleep(2) 

# Print the results
print(f"Total entries extracted: {len(all_data)}")
for name, (birth, death) in all_data:
    if birth and death:
        print(f"Name: {name}, Birth Date: {birth.strip()}, Death Date: {death.strip()}")
    else:
        print(f"Name: {name}, Birth Date: Unknown, Death Date: Unknown")

# Close the driver
driver.quit()


"""


import time
import sys
import re  # Importing the regular expression module
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

first_name = "andrews"
last_name = ""
url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&lastname={last_name}&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1#sr-170512167"

driver = webdriver.Chrome()
driver.get(url)

time.sleep(10)

all_data = []
# For Tracking
previous_result_count = 0

while True:
    # Extract current page content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract all name tags and birth-death dates
    name_tags = soup.find_all('h2', class_='name-grave')
    date_tags = soup.find_all('b', class_='birthDeathDates')


    names = []
    dates = []

    # Extract names
    for tag in name_tags:
        raw_name = tag.get_text(separator=" ", strip=True)

        # Clean up the name
        clean_name = re.sub(r'[“”]', '', raw_name)  # Remove quotes
        clean_name = re.sub(r'[^\w\s,.]', '', clean_name)  # Remove unexpected symbols
        clean_name = re.sub(r'\s{2,}', ' ', clean_name).strip()  # Normalize spaces

        names.append(clean_name)

    # Extract birth and death dates
    for tag in date_tags:
        date_text = tag.get_text(strip=True)


        if date_text == "Birth and death dates unknown.":
            dates.append((None, None)) 
        else:
            # Split dates and remove excess spaces
            birth_date, death_date = [d.strip() for d in date_text.split('–')]
            dates.append((birth_date, death_date))

    # Combine names and dates
    page_data = list(zip(names, dates))

    # Add unique entries
    for entry in page_data:
        if entry not in all_data:
            all_data.append(entry)

    # Check 
    if len(all_data) == previous_result_count:
        print("No more content loaded. Stopping.")
        break

    previous_result_count = len(all_data)

    # Incremental scrolling 
    for _ in range(10): 
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)  

    time.sleep(2)  

print(f"Total entries extracted: {len(all_data)}")
for name, (birth, death) in all_data:
    if birth and death:
        print(f"Name: {name}, Birth Date: {birth.strip()}, Death Date: {death.strip()}")
    else:
        print(f"Name: {name}, Birth Date: Unknown, Death Date: Unknown")


driver.quit()

