from autoscraper import AutoScraper
import csv

# URL to scrape
url = 'https://www.mse.cornell.edu/mse/academic-staff-directory'

# Create an AutoScraper instance
scraper = AutoScraper()

# The first set of example data (a sample of what you want to scrape)
wanted_list = [
    "Rüdiger Dieckmann",  # Example name
    "dieckmann@cornell.edu",  # Example email
    "Materials Science & Engineering"  # Example department
]

# Build the scraper
scraper.build(url, wanted_list)

# Scrape the data
results = scraper.get_result_similar(url, group_by_alias=True)

# Extract and format the information for all faculty members
faculty_list = []
if results:  # Check if results are not empty
    # Group results into sets of three
    data = results.get('', [])  # Access the list of scraped data
    for i in range(0, len(data), 3):  # Assuming there are 3 pieces of data for each faculty member
        name = data[i] if i < len(data) else 'N/A'  # Name
        email = data[i + 1] if i + 1 < len(data) else 'N/A'  # Email
        department = data[i + 2] if i + 2 < len(data) else 'N/A'  # Department
        
        # Append the faculty information as a dictionary
        faculty_list.append({
            'Name': name,
            'Email': email,
            'Department': department
        })

# Specify the CSV file name
csv_file_name = 'cornell_faculty.csv'

# Write to CSV
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Email', 'Department'])
    writer.writeheader()  # Write the header
    for faculty in faculty_list:
        writer.writerow(faculty)  # Write the data

print(f'Data saved to {csv_file_name}')
