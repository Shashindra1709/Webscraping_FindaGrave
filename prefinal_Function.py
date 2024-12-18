import time
import sys
import re
from bs4 import BeautifulSoup
from selenium import webdriver

# Configure stdout to handle Unicode
sys.stdout.reconfigure(encoding='utf-8')

def scrape_findagrave(first_name, last_name, dob=None):
    """
    Scrapes the Find A Grave website for memorials matching the input criteria.
    
    Parameters:
        first_name (str): First name to search for.
        last_name (str): Last name to search for.
        dob (str, optional): Date of birth (YYYY format).
    
    Returns:
        list of tuples: List containing tuples of (Name, Birth Date, Death Date).
    """
    url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&lastname={last_name}&birthyear={dob}&birthyearfilter=&deathyear=&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1#sr-170512167"

    # Start the Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)

    all_data = []
    previous_result_count = 0

    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Remove unwanted tags
        for unwanted_tag in soup.find_all(['span', 'small', 'figure']):
            if (
                'icon-findagrave' in unwanted_tag.get('class', [])
                or 'icon-flowers' in unwanted_tag.get('class', [])
                or 'text-muted' in unwanted_tag.get('class', [])
                or unwanted_tag.get('aria-label') in ['No grave photo', 'Flowers have been left.']
                or 'visually-hidden' in unwanted_tag.get('class', [])
            ):
                unwanted_tag.decompose()

        name_tags = soup.find_all('h2', class_='name-grave')
        date_tags = soup.find_all('b', class_='birthDeathDates')

        names = []
        birth_dates = []
        death_dates = []

        # Extract names
        for tag in name_tags:
            raw_name = tag.get_text(separator=" ", strip=True)
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

        # Scrolling to load content gradually
        for _ in range(10):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(3)

        time.sleep(2)

    driver.quit()
    return all_data


def main():

    first_name = input("Enter the first name: ").strip()
    
    last_name = input("Enter the last name (leave blank if unknown): ").strip()
    dob = input("Enter the year of birth (YYYY, leave blank if unknown): ").strip()
    dob = dob if dob else None

    print(f"Scraping data for: {first_name} {last_name} (DOB: {dob})...")
    data = scrape_findagrave(first_name, last_name, dob)

    for name, birth_date, death_date in data:
        print(f"Name: {name}, Birth Date: {birth_date or 'Unknown'}, Death Date: {death_date or 'Unknown'}")
    print(f"\nTotal entries extracted: {len(data)}")

if __name__ == "__main__":
    main()
