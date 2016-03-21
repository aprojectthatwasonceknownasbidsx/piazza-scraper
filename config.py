import os

get = lambda *args: os.environ.get(*args)

class Config:
    username = get('DB_USERNAME', "dibya.ghosh@g.berkeley.edu")
    password = get('DB_PASSWORD', "piazzascraper")
    courseid = get('COURSEID', "ijkj784v4cs5c8")
