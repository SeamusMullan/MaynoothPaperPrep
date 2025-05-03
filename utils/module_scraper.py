import requests
from bs4 import BeautifulSoup
import json

courses_url = "https://www.maynoothuniversity.ie/international/study-maynooth/available-courses"
department_links = list()

# Fetch all module codes from the available courses page
def fetch_deparments():
    response = requests.get(courses_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        if "available-courses" in href:
            department_links.append(href)

# Fetch all modules from the deparment pages
def fetch_modules():
    modules = []
    for link in department_links:
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('tbody')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) > 2:  # Ensure there are enough columns
                        module = {
                            "name": columns[0].get_text(strip=True),
                            "index": columns[1].get_text(strip=True),
                            "semester": columns[2].get_text(strip=True),
                            "deparment": link.split('/')[-1].replace('-', ' ').title()
                        }
                        modules.append(module)
            else:
                print(f"No <tbody> found for {link}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link}: {e}")

    modules = sorted(modules, key=lambda x: (x['index']))  # Sort by name and index
    return modules

# Run the scraper and save the data to a JSON file
def run():
    fetch_deparments()
    modules = fetch_modules()
    json_data = json.dumps(modules, indent=4)
    with open("modules.json", "w") as f:
        f.write(json_data)
    print("Modules data has been written to modules.json")


if __name__ == "__main__":
    run()