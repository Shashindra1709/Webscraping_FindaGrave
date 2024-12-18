import time
import sys
import re  # Importing the regular expression module
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

# Setup URL
first_name = "andrews"
last_name = ""
url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&{last_name}=&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1#sr-170512167"

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have the correct version of ChromeDriver
driver.get(url)

# Wait for the initial content to load
time.sleep(3)

# Initialize storage for names and dates
all_data = []

# Track the number of results in the last iteration
previous_result_count = 0

while True:
    # Extract current page content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name_tags = soup.select('h2.name-grave')

    # Extract names
    names = []
    for tag in name_tags:
        # Collect visible text, handling nested tags
        raw_name = ''.join(tag.stripped_strings)
        
        # Clean up the name
        clean_name = re.sub(r'[“”]', '', raw_name)  # Remove quotes
        clean_name = re.sub(r'[^\w\s,.]', '', clean_name)  # Remove unexpected symbols
        clean_name = re.sub(r'\s{2,}', ' ', clean_name).strip()  # Normalize spaces
        
        # Handle cases with commas
        if ',' in clean_name:
            # Split by comma and retain the first meaningful part
            clean_name_parts = [part.strip() for part in clean_name.split(',') if part.strip()]
            clean_name = clean_name_parts[0]  # Take only the main part
        
        names.append(clean_name)

    # Extract birth and death dates
    date_tags = soup.select('b.birthDeathDates')
    dates = []

    for tag in date_tags:
        date_text = tag.get_text(strip=True)
        # Handle "unknown" dates case
        if date_text == "Birth and death dates unknown.":
            dates.append((None, None))  # No dates available
        else:
            # Split dates and remove excess spaces
            birth_date, death_date = [date.strip() for date in date_text.split('–')]
            dates.append((birth_date, death_date))

    # Combine names and dates
    page_data = list(zip(names, dates))

    # Add unique entries to the master list
    for entry in page_data:
        if entry not in all_data:
            all_data.append(entry)

    # Check if the number of results has changed
    if len(all_data) == previous_result_count:
        print("No more content loaded. Stopping.")
        break

    previous_result_count = len(all_data)

    # Incremental scrolling to load content gradually
    for _ in range(10):  # Scroll small steps to ensure loader triggers
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)  # Allow partial loading of new content

    time.sleep(2)  # Extra delay to handle dynamic loading

# Print the results
print(f"Total entries extracted: {len(all_data)}")
for name, (birth, death) in all_data:
    if birth and death:
        print(f"Name: {name}, Birth Date: {birth.strip()}, Death Date: {death.strip()}")
    else:
        print(f"Name: {name}, Birth Date: Unknown, Death Date: Unknown")

# Close the driver
driver.quit()
