from datetime import datetime
import re
import html


def remove_tags(text):
    """
    Converts HTML to Python Unicode String
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, "", text)
    return html.unescape(cleantext)


def parse_time(s='2016-03-16T17:31:14Z'):

    """
    Converts Piazza Date-time format into a
    pythonic construct.

    Examples of Piazza Datetime:
    - 2016-03-16T17:31:14Z
    """

    format = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(s,format)

def parse_day(s='01/18'):
    if len(s) < 6:
        s += "/16"
    print(s)
    format = "%m/%d/%y"
    return datetime.strptime(s,format)

def process_all_children(post):
    """
        Flattens comments in a Piazza thread
    """
    return post['children'] + sum([process_all_children(child)
                for child in post['children']], [])
