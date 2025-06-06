# Large Scale Data Scraping

## Introduction
Here are two files that scrape data about influencers from various global pages.<br>
For more details, see the Project Structure section.

## Project Strucutre
<b>1.University Staff Directory Scraper</b>

- <b>Script:</b>`10links.py`
- <b>Description:</b> This script scrapes data about staff from 10 university directory websites at the same time and saves the collected data to a CSV file
- <b>Columns and Data</b>
  - Name
  - Email 
  - Phone Number 
  - University Source URL

- <b>Output:</b> `staff_directory_data.csv`

<b>2.Faculty Directory Scraper</b>
- <b>Script:</b>`uni_autoscrape.py`
- <b>Description:</b>This script uses AutoScraper to extract staff data from a specific university name. 
- <b>Columns and Data:</b>
  - Name
  - Department

- <b>Output:</b> `lboro_faculty.xlsx`


  # Getting started
  ## Usage
  **1.** <b>Clone the Repository</b>
  ```bash
  git clone https://github.com/AslanEmil008/Influencers-Data_scraping.git
  cd Influencers-Data_scraping

  ```
  **2.** <b>Then install `requirments.txt`</b>
  ```bash
  pip install -r requirements.txt
  ```

# How to run
For running `uni_autoscrape.py` you need: <br>
You can find and change the URL to your own in this part of code. 
```bash
url = 'https://www.lborolondon.ac.uk/staff/'
```
Update the wanted_list with the names or titles you want to scrape: 
```bash
wanted_list = ["Charlene Alves", "Advice Consultant"]
```
After making the changes, run the code:

```bash
python3 uni_autoscrape.py
```

For running `10links.py` <br>
You need run it using command:
```bash
python3 10links.py
```






  


