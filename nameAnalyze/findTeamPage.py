import tldextract
from pymongo import MongoClient
from utility import configs as configs
from utility import constants as constants
from utility.utils import formatUrl


def findTeamPages(fileIndex):
    file = configs.getSiteFile(fileIndex)
    client = MongoClient()
    rawDataColl = configs.getScrapedDataColl(client)
    teamPageColl = configs.getTeamPageColl(client)
    # file is opened and each url is read
    with open(file) as sites:
        count = 0
        for url in sites:
            fullUrl = formatUrl(url)
            webColl = rawDataColl.find({"website": fullUrl})
            if (webColl.count() > 0):
                result = teamPage(webColl)
                teamPageColl.update_one({"website": fullUrl},
                                        {"$set": {
                                            "link": result["link"],
                                            "score": result["score"],
                                            "keywords": result['keywords']
                                        }}, upsert=True)

                multiKeywords = result['multiKeywords']
                for key, value in multiKeywords.items():
                    teamPageColl.update_one({"website": fullUrl},
                                            {"$set": {
                                                key: value
                                            }}, upsert=True)

            count = count + 1
            print("findTeamPage process "+ str(fileIndex) + ": "+ str(count) + " website completed")

    client.close()


def teamPage(webColl):
    maxScore = -1
    teamPageLink = ""
    keywords = []
    multiKeywords = {}
    for page in webColl:
        try:
            text = page['webText'].lower()
            link = page['link'].lower()
        except KeyError:
            continue
        curScore = 0
        curKeywords = []
        curMultiKeywords = {}
        if ("team" in link):
            curScore += 3
        if ("about" in link):
            curScore += 1

        for word in constants.team_title:
            word = word.lower()
            if (word in text):
                curScore +=1
                curKeywords.append(word)

        for word in constants.team_title_multi:
            word = word.lower()
            curScore += text.count(word)
            curMultiKeywords[word] = text.count(word)

        if (curScore > maxScore):
            maxScore = curScore
            teamPageLink = page['link']
            keywords = curKeywords
            multiKeywords = curMultiKeywords

    result = dict()
    result["score"] = maxScore
    result["link"] = teamPageLink
    result["keywords"] = keywords
    result['multiKeywords'] = multiKeywords
    return result