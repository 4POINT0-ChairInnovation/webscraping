import os

def getSiteFile(fileIndex):
    location = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))
    if (fileIndex == -1):
        # for single site list with all sites.
        sitesFile = os.path.realpath(os.path.join(location, 'Sites\\NAICS01P.txt'))
    else:
        sitesFile = os.path.realpath(os.path.join(location, 'Sites\\NAICS01P_'+str(fileIndex)+'.txt'))

    return sitesFile


def getInnovCountsColl(client):
    db = client.primer  # database name
    coll = db.aboutus_name_count  #
    return coll


def getScrapedDataColl(client):
    db = client.primer
    coll = db.raw_NAICS54  # reading the raw data after being scraped
    return coll


def getWebRespColl(client):
    db = client.primer
    coll = db.web_resp_aboutus # reading the web response from each URL.
    return coll


def getTeamPageColl(client):
    db = client.primer
    coll = db.VC_team_pages  # the management team page collection
    return coll


def getTeamNameColl(client):
    db = client.primer
    coll = db.VC_names_analyze # the names analyze collection
    return coll