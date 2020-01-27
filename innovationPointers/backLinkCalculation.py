# "backLinkCalculator.py" calculates the backlink count for each website
# Uses MOZ API (url metrics), under the free tier
# MOZ API help : "https://github.com/seomoz/SEOmozAPISamples/tree/master/python"
# API Documentation : "https://moz.com/help/guides/moz-api/mozscape/api-reference/url-metrics"
# Under the free tier, each API call can fetch the backlinks for 10 websites
# A 10 second interval should be present between 2 API calls under the free tier

import os.path
import re
import time

from mozscape import Mozscape
from pymongo import MongoClient
from utility.utils import formatUrl

from utility import configs as configs

# Saves the backLinkCount into a new collection finalMetrics
def saveBacklinkCount(backLinkCount, site, client):
    site = formatUrl(site)
    coll = configs.getInnovCountsColl(client)  # previous collection, the collection to which the backlink count to be appended
    cursor = coll.find_one({'url': site})
    if cursor is not None:
        # cursor['backLinkCount'] = backLinkCount
        # newColl = db.innoPointers_backLinks  # new collection, with backlink count appended
        coll.update_one(cursor,
                        {"$set": {'backLinkCount': backLinkCount}})  # inserting documents into the new collection


def calBackLinkCount(index):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # for testing purpose to limit to 10.
    # file = os.path.join(__location__, '../Sites/sites10.txt')
    file = configs.getSiteFile(index)
    client = MongoClient()
    # A new ACCESS_KEY & SECRET_KEY has to be generated for each new user
    # "https://moz.com/community/join"
    mozClient = Mozscape(
        'mozscape-211f9c0fa5',  # ACCESS ID
        'f38b3766d3d991a4054f38f9746d5d2d'  # SECRET_KEY
    )

    totalLength = sum(1 for line in open(file))
    x = 0
    tempTenSites = []
    counter = 0
    # backLinkObjects = []

    # file is opened and each url is read
    with open(file) as sites:
        for site in sites:
            counter = counter + 1
            site = site.rstrip('\n')

            if (x < 9 or counter == totalLength - 1):  # logic to read 10 websites from the file before calling the API
                tempTenSites.append(site)
                x = x + 1
            else:
                print("Completed for 10 websites..!")
                tempTenSites.append(site)
                # resetting the counter
                x = 0
                # MOZ api free tier has a limit of accessing the api once in 10 seconds
                # Each api call can process 10 websites and respond accordingly
                if counter > 11:
                    time.sleep(10)
                urlMetrics = mozClient.urlMetrics(tempTenSites)  # MOZ API call for url metrics
                for urlMetric in urlMetrics:
                    # backLinkObjects.append(urlMetric)
                    saveBacklinkCount(urlMetric['uid'], urlMetric['uu'], client)
                # empty the temp array
                tempTenSites = []

    print("Backlink calculation completed!!")
    print("Backlink count has been added to innovationCount.")
    client.close()