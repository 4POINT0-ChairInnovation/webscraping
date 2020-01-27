import re


def formatUrl(link):
    link = link.strip('\n')
    link = re.sub('((http|https)://www.)|www.|(https://|http://)', "", link.rstrip('\n'))
    link = link.rstrip('/')
    return link