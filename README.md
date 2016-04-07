# Piazza Scraper

Scrapes [piazza.com](http://piazza.com).

# Installation

Create a conda environment using

	conda create --name ENV_NAME python=3.4

Install `piazza-api` from source, using `pip`.

	pip install git+https://github.com/bidsX/piazza-api3.git

Install from the list of requirements.

	pip install -r requirements.txt

# How to Run

To run the scraper, do the following. We assume that you have already started your conda environment using

	source activate ENV_NAME

1) If the database hasn't already been created (e.g. this is the first time you are running the scraper), run

	python models.py

2) To run the scraper, run

	python scraper.py

3) Whenever you want to refetch pages, run the scraper again, or use the following argument -r to pick some time to get info from
	
	python scraper.py -r 2 (2 days of overlap)

# Development

The project structure is as following

- models.py - Models for SQLAlchemy ORM
- config.py - User/Password/Class ID info for Piazza
- utils.py  - Helpful utilities for parsing Piazza blocks
- scraper.py - The main scraper/store to database
