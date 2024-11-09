from autoscraper import AutoScraper

# URL to scrape
url = 'https://ed.stanford.edu/faculty/directory'

# Create an AutoScraper instance
scraper = AutoScraper()

# The first set of example data (a sample of what you want to scrape)
wanted_list = [
    "Subini Annamma",  # Example name
    "Associate Professor",  # Example title
    "subini@stanford.edu",  # Example email
    "(650) 498-1448"  # Example phone number
]

# Build the scraper
scraper.build(url, wanted_list)

# Scrape the data
results = scraper.get_result_similar(url, group_by_alias=True)

# Print the results to check the structure
print(results)

# Use a set to collect unique faculty members
faculty_set = set()

# Extract and format the information for all faculty members
if results:  # Check if results are not empty
    for i in range(len(results.get('name', []))):
        name = results.get('name', [None])[i] or 'none'
        title = results.get('title', [None])[i] or 'none'
        email = results.get('email', [None])[i] or 'none'
        phone = results.get('phone', [None])[i] or 'none'
        
        # Create a faculty entry tuple
        faculty_entry = (name, title, email, phone)

        # Add to the set to avoid duplicates
        faculty_set.add(faculty_entry)

# Print the formatted results without duplicates
for faculty in faculty_set:
    print(','.join(faculty))




