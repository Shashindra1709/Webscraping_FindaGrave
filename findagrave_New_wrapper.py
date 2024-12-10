import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def scrape_data(first_name, last_name="", birth_year="", death_year="", death_year_filter="", location=""):
    """
    Scrapes data from Find A Grave website based on the provided parameters.

    Args:
        first_name (str): First name of the individual.
        last_name (str): Last name of the individual (optional).
        birth_year (str): Birth year filter (optional).
        death_year (str): Death year filter (optional).
        death_year_filter (str): Filter for +/- range around death year (optional).
        location (str): Location filter (optional).

    Returns:
        list: A list of tuples containing names, birth dates, death dates, and location.
    """
    url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&lastname={last_name}" \
          f"&birthyear={birth_year}&birthyearfilter=&deathyear={death_year}&deathyearfilter={death_year_filter}&location={location}" \
          f"&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1"

    # Set up the web driver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)

    all_data = []
    previous_result_count = 0

    try:
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Remove unwanted tags
            for unwanted_tag in soup.find_all(['span', 'small', 'figure']):
                if ('icon-findagrave' in unwanted_tag.get('class', []) or
                        'icon-flowers' in unwanted_tag.get('class', []) or
                        'text-muted' in unwanted_tag.get('class', []) or
                        unwanted_tag.get('aria-label') in ['No grave photo', 'Flowers have been left.'] or
                        'visually-hidden' in unwanted_tag.get('class', [])):
                    unwanted_tag.decompose()

            # Extract name, date, and location information
            name_tags = soup.find_all('h2', class_='name-grave')
            date_tags = soup.find_all('b', class_='birthDeathDates')
            location_divs = soup.find_all('div', class_='memorial-item---cemet')

            names, birth_dates, death_dates, locations = [], [], [], []

            for tag in name_tags:
                raw_name = tag.get_text(separator=" ", strip=True)
                clean_name = re.sub(r'[“”]', '', raw_name)
                clean_name = re.sub(r'[^\w\s,.]', '', clean_name)
                clean_name = re.sub(r'\s{2,}', ' ', clean_name).strip()
                names.append(clean_name)

            for tag in date_tags:
                date_text = tag.get_text(strip=True)
                if date_text == "Birth and death dates unknown.":
                    birth_dates.append(None)
                    death_dates.append(None)
                else:
                    birth_date, death_date = [d.strip() for d in date_text.split('–')]
                    birth_dates.append(birth_date)
                    death_dates.append(death_date)

            # Extract location information and clean it
            for div in location_divs:
                location_tag = div.find('p', class_='addr-cemet', string=lambda x: x and 'Plot info:' not in x)
                if location_tag:
                    # location_text = location_tag.get_text(separator=" ", strip=True).replace('\n', '').replace('  ', ' ')
                    location_text = " ".join(location_tag.get_text(separator=" ", strip=True).split())
                    locations.append(location_text)
                else:
                    locations.append(None)


            # Ensure lists have the same length
            while len(locations) < len(names):
                locations.append(None)

            page_data = list(zip(names, birth_dates, death_dates, locations))

            # Add unique entries
            for entry in page_data:
                if entry not in all_data:
                    all_data.append(entry)

            if len(all_data) == previous_result_count:
                print("No more content loaded. Stopping.")
                break

            previous_result_count = len(all_data)

            # Scroll to load more content
            for _ in range(10):
                driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(3)

            time.sleep(2)

    finally:
        driver.quit()

    return all_data


# Main program
if __name__ == "__main__":
    # Get input from the user
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name (optional): ").strip()
    birth_year = input("Enter birth year (optional): ").strip()
    death_year = input("Enter death year (optional): ").strip()

    # Input for death year filter
    death_year_filter = input("Enter +/- range for death year filter (e.g., +1, -1, +2): ").strip()

    location = input("Enter location (optional): ").strip()

    # Call the wrapper function
    data = scrape_data(first_name, last_name, birth_year, death_year, death_year_filter, location)

    # Display the results
    print(f"Total entries extracted: {len(data)}")
    for name, birth_date, death_date, loc in data:
        location_info = f"Location: {loc}" if loc else "Location: Unknown"
        print(f"Name: {name}, Birth Date: {birth_date or 'Unknown'}, Death Date: {death_date or 'Unknown'}, {location_info}")

    # Save the results
    # save_csv = input("Do you want to save the data to a CSV file? (y/n): ").strip().lower()
    # if save_csv == "y":
    #     df = pd.DataFrame(data, columns=["Name", "Birth Date", "Death Date", "Location"])
    #     output_file = "findagrave_data.csv"
    #     df.to_csv(output_file, index=False, encoding='utf-8')
    #     print(f"Data saved to {output_file}.")
