from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient
from nltk.tag import StanfordNERTagger
from nameparser import HumanName
import os
import nameAnalyze.genderAnalyzer as genderAnalyzer
from utility import configs as configs
from utility.utils import formatUrl


def insert_aboutus_db(client, personsList, doc):
    coll = configs.getTeamNameColl(client)
    link = doc['link']
    website = doc['website']
    for person in personsList:
        name = person['name']
        lastName = person["last_name"]
        firstName = person["first_name"]
        gender = person["gender"]
        usaGender = person["usa_gender"]
        title = person["title"]
        orderIndex = person["order_index"]
        coll.update_one({"link": link, "website": website, "name": name},
                        {"$set": {
                            "last_name": lastName,
                            "first_name": firstName,
                            "usaGender": usaGender,
                            "gender": gender,
                            "title": title,
                            "orderIndex": orderIndex
                        }}, upsert=True)


def explore_title_name(link, client):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    rawDataColl = configs.getScrapedDataColl(client)
    cursor = rawDataColl.find({"link": link})
    NER_CLASSIFIERS_PATH = os.path.join(dir_path, "english.all.3class.distsim.crf.ser.gz")
    NER_JAR_PATH = os.path.join(dir_path, "stanford-ner.jar")
    os.environ['JAVAHOME'] = "C:\ProgramData\Oracle\Java\javapath\java.exe"
    nlp_tagger = StanfordNERTagger(NER_CLASSIFIERS_PATH, NER_JAR_PATH)

    for doc in cursor:
        try:
            raw_text = doc['webText']
        except KeyError:
            continue
        raw_text = raw_text.replace('/', ' ')
        raw_text_list = raw_text.split('\n')
        sent_tokenize_list = []
        for raw in raw_text_list:
            if (len(raw) > 0):
                sent_tokenize_list.append(sent_tokenize(raw))

        tokenized_sentences = []
        for sentence in sent_tokenize_list:
            if len(sentence) > 0:
                tokenized_sentences.append(word_tokenize(sentence[0]))

        tagged_sentences = []
        for sentence in tokenized_sentences:
            tagged_sentences.append(nlp_tagger.tag(sentence))

        personsList = genderAnalyzer.title_name_search(tagged_sentences)
        orderIndex = 1
        for person in personsList:
            result = HumanName(person['name'])
            person["last_name"] = result.last
            person["first_name"] = result.first
            genderResult =  genderAnalyzer.analyze_gender(result.first)
            person["gender"] = genderResult["gender"]
            person["usa_gender"] = genderResult["usa_gender"]
            person["order_index"] = orderIndex
            orderIndex += 1

        insert_aboutus_db(client, personsList, doc)


def explore_team_pages(fileIndex):
    client = MongoClient()
    file = configs.getSiteFile(fileIndex)
    teamPageColl = configs.getTeamPageColl(client)
    count = 0
    with open(file) as sites:
        for url in sites:
            fullUrl = formatUrl(url)
            cursor = teamPageColl.find({"website": fullUrl})
            if (cursor.count() > 0):
                for doc in cursor:
                    link = doc['link']
                    explore_title_name(link, client)
            count = count + 1
            print("findTeamPage process "+ str(fileIndex) + ": "+ str(count) + " website completed")

    # close the connection
    client.close()