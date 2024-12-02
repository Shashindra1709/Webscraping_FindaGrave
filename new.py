"""import sys
import sys
import requests
from bs4 import BeautifulSoup

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

first_name = "andrews"
last_name = ""
url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&{last_name}=&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1#sr-170512167"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

# Send a request with headers
response = requests.get(url, headers=headers)



if response.status_code == 200:
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response.status_code)
    # Print the soup text directly
    soup.prettify()
    
    names = [i_tag.get_text(strip=True) for i_tag in soup.select('h2.name-grave i')]
    print(names)
    print(len(names))
    
else:
    print("Failed to retrieve the page")
"""


import sys
import requests
from bs4 import BeautifulSoup

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

first_name = "andrews"
last_name = ""
url = f"https://www.findagrave.com/memorial/search?firstname={first_name}&middlename=&{last_name}=&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=r&page=1#sr-170512167"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}


response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response.status_code)

    # Extract names
    names =[]
    
    for i_tag in soup.select('h2.name-grave i'):
        a= i_tag.get_text(strip=True)
        names.append(a)

    # Extract birth and death dates
    dates = []
    for b_tag in soup.select('b.birthDeathDates'):
        date_text = b_tag.get_text(strip=True)
        birth_date, death_date = [date.strip() for date in date_text.split('–')]
        dates.append((birth_date, death_date))

    # Combine names with their corresponding dates
    results = list(zip(names, dates))

    # Print the results
    for name, (birth, death) in results:
        print(f"Name: {name}, Birth Date: {birth}, Death Date: {death}")

    # Summary
    print(f"\nTotal names extracted: {len(names)}")

else:
    print("Failed to retrieve the page")



# import requests
# from bs4 import BeautifulSoup

# # Base URL (adjust if needed)
# base_url = "https://www.findagrave.com/memorial/search"

# # Parameters for the request
# params = {
#     "firstname": "andrews",
#     "lastname": "",
#     "page": 1,  # Start from the first page
# }

# # Headers to mimic a browser
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
# }

# # List to store all extracted names
# all_names = []

# while True:
#     # Send the request
#     response = requests.get(base_url, headers=headers, params=params)

#     if response.status_code != 200:
#         print(f"Failed to fetch page {params['page']}. Status code: {response.status_code}")
#         break

#     # Parse the content
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Extract names from the current page
#     names = [i_tag.get_text(strip=True) for i_tag in soup.select('h2.name-grave i')]
#     if not names:
#         print("No more names found.")
#         break

#     # Add to the list of all names
#     all_names.extend(names)

#     print(f"Page {params['page']} - Extracted {len(names)} names.")

#     # Check if there's a next page indicator
#     next_page = soup.find('h2', id=f"srppage{params['page'] + 1}")
#     if not next_page:
#         print("Reached the last page.")
#         break

#     # Increment the page number for the next request
#     params['page'] += 1

# # Print the total count of names and sample names
# print(f"Total names extracted: {len(all_names)}")
# print("Sample names:", all_names[:10])  # Print the first 10 names

