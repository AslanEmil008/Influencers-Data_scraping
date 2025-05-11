from autoscraper import AutoScraper
import pandas as pd

# URL to scrape
url = 'https://www.lborolondon.ac.uk/staff/'

# The data you want to extract
wanted_list = ["Charlene Alves", "Advice Consultant"]

# Create scraper and build
scraper = AutoScraper()
scraper.build(url, wanted_list)

# Get results
results = scraper.get_result_similar(url, group_by_alias=True)

# Extract and format
faculty_list = []
if results:
    data = results.get('', [])
    for i in range(0, len(data), 2):  # 2 items: name and department
        name = data[i] if i < len(data) else 'N/A'
        department = data[i + 1] if i + 1 < len(data) else 'N/A'
        faculty_list.append({'Name': name, 'Department': department})

# Save to Excel using pandas
df = pd.DataFrame(faculty_list)
xlsx_file_name = 'lboro_faculty.xlsx'
df.to_excel(xlsx_file_name, index=False)

print(f'Data saved to {xlsx_file_name}')
