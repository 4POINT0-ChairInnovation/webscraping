import nameAnalyze.findNameOnPage as aboutus
from utility import configs as configs
from pymongo import MongoClient

client = MongoClient()
coll = configs.getScrapedDataColl(client)
listOfLink = coll.distinct("link")
#for link in listOfLink:
link = "http://www.aviditybiosciences.com/about/management-team/"
aboutus.explore_title_name(link)
client.close()