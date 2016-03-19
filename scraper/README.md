## Piazza Scraper

This is a python scraper for Piazza to save to 
a database

The main file is scraper.py:

To run the scraper, do the following

1) If the database hasn't already been created (e.g. this is the first time you are running the scraper), run

python models.py

2) To run the scraper, run

python -i scraper.py 

>> s = Scraper()
>> s.get(100) #Saves 100 posts to database
