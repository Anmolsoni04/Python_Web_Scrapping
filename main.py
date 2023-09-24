import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the website to scrape
base_url = "https://intake.steerhealth.io/doctor-search/aa1f8845b2eb62a957004eb491bb8ba70a"

# Initialize a list to store provider details
provider_details = []

# Loop through all pages (assuming you need to scrape multiple pages)
page_number = 1

while True:
    url = f"{base_url}?page={page_number}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and loop through provider information on the page
        provider_cards = soup.find_all('div', class_='provider-item')

        for provider in provider_cards:
            name = provider.find('h2', class_='provider-title').text.strip()
            title = provider.find('p', class_='provider-subtitle').text.strip()
            gender = provider.find('div', class_='provider-gender').text.strip()
            expertise = provider.find('div', class_='provider-specialty').text.strip()
            research_interests = provider.find('div', class_='provider-research-interests').text.strip()
            phone = provider.find('div', class_='provider-phone').text.strip()
            location = provider.find('div', class_='provider-location').text.strip()
            education = provider.find('div', class_='provider-education').text.strip()

            provider_info = {
                'Name': name,
                'Title': title,
                'Gender': gender,
                'Expertise': expertise,
                'Research Interests': research_interests,
                'Phone': phone,
                'Location': location,
                'Education': education
            }

            provider_details.append(provider_info)

        # Check if there are more pages to scrape
        next_page = soup.find('li', class_='page-item', string='Next')
        if not next_page:
            break

        page_number += 1
    else:
        print(f'Failed to retrieve page {page_number}')
        break

# Store the provider details in a CSV file
with open('providers.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Title', 'Gender', 'Expertise', 'Research Interests', 'Phone', 'Location', 'Education']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for provider_info in provider_details:
        writer.writerow(provider_info)

print(f'Scraping completed. {len(provider_details)} profiles saved to providers.csv')


