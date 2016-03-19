## Piazza Scraper

This is a python scraper for Piazza to save to 
a database

The main file is scraper.py

To run the scraper, do the following

1) If the database hasn't already been created (e.g. this is the first time you are running the scraper), run

	python models.py

2) To run the scraper, run

	python -i scraper.py 

In the interpreter:

	s = Scraper()
	s.get(100) #Saves 100 posts to database



#### Development
The project structure is as following

- models.py - Models for SQLAlchemy ORM
- config.py - User/Password/Class ID info for Piazza
- utils.py  - Helpful utilities for parsing Piazza blocks
- scraper.py - The main scraper/store to database