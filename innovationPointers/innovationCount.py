# "innovationCount.py" cleans the raw data scraped and stores it back into a new document in the database
# This is the most important and the powerful module, which holds the capability to parse and extract the innovation pointers
import os.path
import re
import innovationScraping.utility.constants as const
import tldextract
from pymongo import MongoClient
import innovationScraping.innovationPointers.CleanedItem as cleanedItem
from innovationScraping.utility import configs as configs
from innovationScraping.utility.utils import formatUrl
import logging
logging.basicConfig(filename='multiProcessData52.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.info('Start multi data processing')

# method accumulating the count of  keywords from the raw data
def getStats(cursor):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    innodict = os.path.join(__location__, '../Dictionaries/InnovationDict.txt')
    RandDDict = os.path.join(__location__, '../Dictionaries/RandDDict.txt')
    TechDict = os.path.join(__location__, '../Dictionaries/TechDict.txt')
    StrategyDict = os.path.join(__location__, '../Dictionaries/StrategyDict.txt')
    PatentDict = os.path.join(__location__, '../Dictionaries/PatentDict.txt')
    DesignDict = os.path.join(__location__, '../Dictionaries/ProductFunction.txt')
    FonctionDict = os.path.join(__location__, '../Dictionaries/ProductDesign.txt')
    LunchdDict = os.path.join(__location__, '../Dictionaries/NewProductLunch.txt')

    twitter_link_1 = "www.twitter.com/"
    twitter_link_2 = "twitter.com/"
    twitter_link_3 = "twitter.com"

    global line
    item = cleanedItem.CleanedItem()
    count = cursor.count(with_limit_and_skip=False)
    item.numInnerUrls = count
    print("here")
    for i in cursor:
        # etl functionality goes here
        try:
            text = i['webText']
            webContent = i['webContent']
            webWords = webContent.split()
            words = text.split()
            innerUrl = i['link']
        except KeyError:
            continue

        # Check for twitter accounts
        for word in words:
            if twitter_link_1 in word or twitter_link_2 in word or twitter_link_3 in word:
                item.twitter_accounts.append(word)

        for word in webWords:
            if twitter_link_1 in word or twitter_link_2 in word or twitter_link_3 in word:
                item.twitter_accounts.append(word)

        # Counting the total frequency of keywords in each WEBSITE content and innerUrl

        with open(DesignDict) as x:
            for line in x:
                if line in innerUrl:
                    item.DesignPageCount = item.DesignPageCount + 1  # inno1 : Count of innovation pages
                item.DesignOccurenceCount = item.DesignOccurenceCount + text.count(line)  # inno2: Count of innovation term in whole the website
        with open(FonctionDict) as x:
            for line in x:
                if line in innerUrl:
                    item.FonctionPageCount = item.FonctionPageCount + 1  # inno1 : Count of innovation pages
                item.FonctionOccurenceCount = item.FonctionOccurenceCount + text.count(line)  # inno2: Count of innovation term in whole the website
        with open(LunchdDict) as x:
            for line in x:
                if line in innerUrl:
                    item.LunchPageCount = item.LunchPageCount + 1  # inno1 : Count of innovation pages
                item.LunchPageCount = item.LunchPageCount + text.count(line)  # inno2: Count of innovation term in whole the website
        with open(PatentDict) as x:
            for line in x:
                if line in innerUrl:
                    item.patentPageCount = item.patentPageCount + 1  # inno1 : Count of innovation pages
                item.patentOccurrenceCount = item.patentOccurrenceCount + text.count(line)  # inno2: Count of innovation term in whole the website
        with open(innodict) as l:
            for line in l:
                if line in innerUrl:
                    item.innovationPageCount = item.innovationPageCount + 1  # inno1 : Count of innovation pages
                item.innovationOccurrenceCount = item.innovationOccurrenceCount + text.count(
                    line)  # inno2: Count of innovation term in whole the website
        with open(RandDDict) as p:
            for line in p:
                if line in innerUrl:
                    item.RandDPageCount = item.RandDPageCount + 1  # RD1 : Count of RandD pages
                item.RandDOccurenceCount = item.RandDOccurenceCount + text.count(
                    line)  # RD2: Count of RandD term in whole the website
        with open(TechDict) as p:
            for line in p:
                if line in innerUrl:
                    item.TechPageCount = item.TechPageCount + 1  # Tec1 : Count of Technology pages
                item.TechOccurenceCount = item.TechOccurenceCount + text.count(
                    line)  # Tec2: Count of Technology term in whole the website
        with open(StrategyDict) as p:
            for line in p:
                if line in innerUrl:
                    item.StrategyPageCount = item.StrategyPageCount + 1  # Str1 : Count of Strategy pages
                item.StrategyOccurenceCount = item.StrategyOccurenceCount + text.count(
                    line)  # Str2: Count of Strategy term in whole the website

        single_line_text = ""
        for line in text.splitlines():
            single_line_text = single_line_text + " " + line.strip()

        for code in re.finditer(const.postal_code_pat, single_line_text):
            if code.group(0) not in item.post_codes:
                item.post_codes.append(code.group(0))

            startIndex = code.start(0)
            startIndex = startIndex - 100
            endIndex = code.end(0)
            sub_search = single_line_text[startIndex:endIndex]
            for address in re.finditer(const.street_no_pat, sub_search, re.UNICODE):
                startIndex = address.start()
                address =  sub_search[startIndex:endIndex].strip()
                if (address not in item.addresses) and (len(address) > 0):
                    item.addresses.append(address)

        for prov in re.finditer(const.province_pat, single_line_text, re.UNICODE):
            if prov.group(0) not in item.provinces:
                item.provinces.append(prov.group(0))

            if len(item.post_codes) == 0:
                startIndex = prov.start(0) - 100
                endIndex = prov.end(0)
                sub_search = single_line_text[startIndex:endIndex]

                for address in re.finditer(const.street_no_pat, sub_search, re.UNICODE):
                    startIndex = address.start()
                    address = sub_search[startIndex:endIndex].strip()
                    if (address not in item.addresses) and (len(address) > 0):
                        item.addresses.append(address)

    return item


# saves the cleaned documents into the database
def saveCleanedItem(item, client):
    coll = configs.getInnovCountsColl(client) # new collection cleanedData

    coll.update_one({"url": item.url}, {"$set" : {
        "patentPageCount": item.patentPageCount,
        "patentOccurrenceCount": item.patentOccurrenceCount,
        "innovationPageCount": item.innovationPageCount,
        "innovationOccurrenceCount": item.innovationOccurrenceCount,
        "RandDPageCount": item.RandDPageCount,
        "RandDOccurenceCount": item.RandDOccurenceCount,
        "TechPageCount": item.TechPageCount,
        "TechOccurenceCount": item.TechOccurenceCount,
        "StrategyPageCount": item.StrategyPageCount,
        "StrategyOccurenceCount": item.StrategyOccurenceCount,
        "innerUrlCount": item.numInnerUrls,
        "DesignPageCount": item.DesignPageCount,
        "DesignOccurenceCount": item.DesignOccurenceCount,
        "FonctionPageCount": item.FonctionPageCount,
        "FonctionOccurenceCount": item.FonctionOccurenceCount,
        "LunchPageCount": item.LunchPageCount,
        "LunchOccurenceCount": item.LunchOccurenceCount,
        "twitter_accounts": item.twitter_accounts,
        "company": item.comp,
        "addresses": item.addresses,
        "postal_codes": item.post_codes,
        "provinces": item.provinces
    }}, upsert=True)


def calInnovCount(fileIndex):
    # openning 'innovation', 'R&D', 'Technology', 'Strategy' dictionaries
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # file = os.path.join(__location__, '../Sites/sites10.txt')
    file = configs.getSiteFile(fileIndex)
    client = MongoClient()
    coll = configs.getScrapedDataColl(client)

    # file is opened and each url is read
    with open(file) as sites:
        count = 0
        for url in sites:
            fullUrl = formatUrl(url)
            callCursor = coll.find(
                {
                    "website": fullUrl
                }
            )
            if (callCursor.count() > 0):
                item = getStats(callCursor)
                item.url = fullUrl

                ext = tldextract.extract(url)
                item.comp = ext.domain

                saveCleanedItem(item, client)

            count = count + 1
            print("process "+ str(fileIndex) + ": "+ str(count) + " website completed")

    client.close()