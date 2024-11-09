import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# URLs to scrape
urls = [
    "https://gsas.yale.edu/about/staff-directory",
    "https://college.uchicago.edu/about/college-staff-directory",
    "https://gradschool.cornell.edu/about/staff-directory/",
    "https://www.mse.cornell.edu/mse/academic-staff-directory",
    "https://law.duke.edu/directory/",
    "https://education.washington.edu/about/directory",
    "https://english.washington.edu/people",
    "https://ism.ku.dk/contact/employees/",
    "https://www.library.dartmouth.edu/directory",
    "https://education-sport.ed.ac.uk/about-us/people/academic-staff-a-z"
]

# Initialize an empty list to store extracted data
data = []

# Function to scrape each URL
def scrape_url(url):
    print(f"Scraping URL: {url}")  # Log the current URL
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    try:
        # Use Selenium to access the page
        driver.get(url)

        # Give the page some time to load
        time.sleep(5)  # Increased wait time for page load

        # Scroll to load more content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # If no new content, exit the loop
            last_height = new_height

        # Use BeautifulSoup to parse the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract data based on specific HTML structure for each URL
        if "gsas.yale.edu" in url:
            for entry in soup.select('.contacts'):
                name = entry.select_one('.h4').get_text(strip=True) if entry.select_one('.h4') else "None"
                phone = entry.select_one('a[href^="tel:"]').get_text(strip=True) if entry.select_one('a[href^="tel:"]') else "None"
                email = entry.select_one('a[href^="mailto:"]').get_text(strip=True) if entry.select_one('a[href^="mailto:"]') else "None"
                data.append({"Name": name, "Phone": phone, "Email": email})

        elif "college.uchicago.edu" in url:
            for entry in soup.select('li'):  # Select all <li> elements
                name = entry.select_one('h3.t-heading--small').get_text(strip=True) if entry.select_one('h3.t-heading--small') else "None"
                phone = entry.select_one('a[href^="tel:"]').get_text(strip=True) if entry.select_one('a[href^="tel:"]') else "None"
                email = entry.select_one('a[href^="mailto:"]').get_text(strip=True) if entry.select_one('a[href^="mailto:"]') else "None"
                data.append({"Name": name, "Phone": phone, "Email": email})

        elif "gradschool.cornell.edu" in url:
            for entry in soup.select('tr[class^="row-"]'):
                name = entry.select_one('td.column-1').get_text(strip=True) if entry.select_one('td.column-1') else "None"
                email = entry.select_one('td.column-2 a').get_text(strip=True) if entry.select_one('td.column-2 a') else "None"
                phone = entry.select_one('td.column-3').get_text(strip=True) if entry.select_one('td.column-3') else "None"
                data.append({"Name": name, "Phone": phone, "Email": email})

        elif "mse.cornell.edu" in url:
            for entry in soup.select('.faculty-info'):
                name = entry.select_one('.person__name span').get_text(strip=True) if entry.select_one('.person__name span') else "None"
                phone = entry.select_one('.person__phone a').get_text(strip=True) if entry.select_one('.person__phone a') else "None"
                email = entry.select_one('.person__email a').get_text(strip=True) if entry.select_one('.person__email a') else "None"
                data.append({"Name": name, "Phone": phone, "Email": email})

        elif "law.duke.edu" in url:
            for entry in soup.select('.directory-information'):
                name = entry.select_one('.directory-name a').get_text(strip=True) if entry.select_one('.directory-name a') else "None"
                phone = entry.select_one('.directory-phone').get_text(strip=True).replace(' ', '') if entry.select_one('.directory-phone') else "None"
                email = entry.select_one('.directory-email a').get_text(strip=True) if entry.select_one('.directory-email a') else "None"
                data.append({"Name": name, "Phone": phone, "Email": email})

        elif "education.washington.edu" in url:
            for entry in soup.select('tr'):
                name = entry.select_one('.views-field-title a').get_text(strip=True) if entry.select_one('.views-field-title a') else "None"
                email = entry.select_one('.views-field-field-email a').get_text(strip=True) if entry.select_one('.views-field-field-email a') else "None"
                data.append({"Name": name, "Email": email})

        elif "english.washington.edu" in url:
            for entry in soup.select('tr'):
                name = entry.select_one('td.views-field-field-last-name a').get_text(strip=True) if entry.select_one('td.views-field-field-last-name a') else "None"
                email = entry.select_one('td.views-field-field-email a[href^="mailto:"]').get_text(strip=True) if entry.select_one('td.views-field-field-email a[href^="mailto:"]') else "None"
                phone = entry.select_one('td.views-field-field-email a[href^="tel:"]').get_text(strip=True) if entry.select_one('td.views-field-field-email a[href^="tel:"]') else "None"
                data.append({"Name": name, "Phone": phone, "Email": email})

        elif "ku.dk" in url:
            entries = soup.select('tr.odd, tr.even')
            for entry in entries:
                name_elem = entry.select_one('td.emplistname a')
                name = name_elem.get_text(strip=True) if name_elem else "None"

                email_elem = entry.select_one('td.emplistemail a')
                if email_elem:
                    email = email_elem.get('onmouseover', "None").replace("this.title=", "").replace("'; return true;", "").strip().strip('"')
                else:
                    email = "None"

                phone_elem = entry.select_one('td.emplistphone')
                phone = phone_elem.get_text(strip=True) if phone_elem else "None"

                data.append({"Name": name, "Email": email, "Phone": phone})

        elif "library.dartmouth.edu" in url:
            for entry in soup.select('.profile-item'):
                name = entry.select_one('.title a').get_text(strip=True) if entry.select_one('.title a') else "None"
                phone = entry.select_one('a[href^="tel:"]').get_text(strip=True) if entry.select_one('a[href^="tel:"]') else "None"
                email = entry.select_one('.email a').get_text(strip=True) if entry.select_one('.email a') else "None"
                data.append({"Name": name, "Phone": phone, "Email": email})

        elif "education-sport.ed.ac.uk" in url:
            for entry in soup.select('tr'):
                name = entry.select_one('td a').get_text(strip=True) if entry.select_one('td a') else "None"
                email = entry.select_one('td a[href^="mailto:"]').get_text(strip=True) if entry.select_one('td a[href^="mailto:"]') else "None"
                phone = entry.select_one('td').find_next_sibling().get_text(strip=True) if entry.select_one('td') and entry.select_one('td').find_next_sibling() else "None"
                data.append({"Name": name, "Email": email, "Phone": phone})

    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
    finally:
        driver.quit()  # Close the browser after scraping

# Iterate over URLs and scrape
for url in urls:
    scrape_url(url)

# Create a DataFrame and export to CSV
df = pd.DataFrame(data)
df.to_csv("staff_directory_data.csv", index=False)
print("Data exported to staff_directory_data.csv")
