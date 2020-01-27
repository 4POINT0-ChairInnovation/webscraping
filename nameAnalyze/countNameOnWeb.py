from utility import configs as configs
from pymongo import MongoClient
from utility.utils import formatUrl

def count_name_on_web(fileIndex):
    client = MongoClient()
    file = configs.getSiteFile(fileIndex)
    rawDataColl = configs.getScrapedDataColl(client)
    teamNameColl = configs.getTeamNameColl(client)
    with open(file) as sites:
        count = 0
        for url in sites:
            website = formatUrl(url)
            fullNameList = teamNameColl.find({"website": website}).distinct("name")
            firstNameList = teamNameColl.find({"website": website}).distinct("first_name")
            lastNameList = teamNameColl.find({"website": website}).distinct("last_name")
            rawTxtCursor = rawDataColl.find({"website": website}, {'webText':1})

            fullNameCounts = {}
            firstNameCounts = {}
            lastNameCounts = {}

            for doc in rawTxtCursor:
                # count full name occurrences
                for word in fullNameList:
                    if word not in fullNameCounts:
                        fullNameCounts[word] = 0

                    fullNameCounts[word]  += doc['webText'].count(word)

                # count first name occurrences
                for word in firstNameList:
                    if word not in firstNameCounts:
                        firstNameCounts[word] = 0

                    firstNameCounts[word]  += doc['webText'].count(word)

                # count last name occurrences
                for word in lastNameList:
                    if word not in lastNameCounts:
                        lastNameCounts[word] = 0

                    lastNameCounts[word] += doc['webText'].count(word)

            update_full_name(website, fullNameCounts, client)
            update_first_name(website, firstNameCounts, client)
            update_last_name(website, lastNameCounts, client)
            count += 1
            print("countName process "+ str(fileIndex) + ": "+ str(count) + " website completed")

    client.close()


def update_full_name(website, fullNameCounts, client):
    teamNameColl = configs.getTeamNameColl(client)
    for name, count in fullNameCounts.items():
        teamNameColl.update({"website": website, "name": name},
                                {"$set": {
                                    "full_name_count":count
                                }}, upsert=True, multi=True)


def update_first_name(website, firstNameCounts, client):
    teamNameColl = configs.getTeamNameColl(client)
    for name, count in firstNameCounts.items():
        teamNameColl.update({"website": website, "first_name": name},
                                {"$set": {
                                    "first_name_count":count
                                }}, upsert=True, multi=True)


def update_last_name(website, lastNameCounts, client):
    teamNameColl = configs.getTeamNameColl(client)
    for name, count in lastNameCounts.items():
        teamNameColl.update({"website": website, "last_name": name},
                                {"$set": {
                                    "last_name_count":count
                                }}, upsert=True, multi=True)
