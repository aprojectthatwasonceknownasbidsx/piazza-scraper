import os

get = lambda *args: os.environ.get(*args)

class Config:
    username = get('DB_USERNAME', "dibya.ghosh@g.berkeley.edu")
    password = get('DB_PASSWORD', "")
    courseid = get('COURSEID', "hyq0br1u3kx7dg")
