import gender_guesser.detector as gender

from utility.constants import real_title_words

detector =  gender.Detector()

#Attempt to analyze the gender based on first Name
def analyze_gender(firstName):
    gender = detector.get_gender(firstName)
    usa_gender = detector.get_gender(firstName, "usa")
    result = dict()
    result['gender'] = gender
    result['usa_gender'] = usa_gender
    return result

"""
Get the name and possible title from a web page.
"""
def title_name_search(tagged_sentences):
    personsList = []
    for i, sentence in enumerate(tagged_sentences):
        # if there are more than 2 words in this sentences belongs to person.
        possible_title_words_1 = []
        possible_title_words_2 = []
        possible_title_words_3 = []
        if (len([word for word in sentence if word[1] == "PERSON"]) >= 2):
            if (i + 2) < len(tagged_sentences):
                possible_title_words_3 = [element[0].replace("\n", "").replace("\t", "").strip() for element in tagged_sentences[i + 2] if ((element[1] != "PERSON") and (len(element[0].strip())) > 1)]

            if (i + 1) < len(tagged_sentences):
                possible_title_words_1 = [element[0].replace("\n", "").replace("\t", "").strip() for element in tagged_sentences[i + 1] if ((element[1] != "PERSON") and (len(element[0].strip())) > 1)]

            possible_title_words_2 = [element[0].replace("\n", "").replace("\t", "").strip() for element in sentence if ((element[1] != "PERSON") and (len(element[0].strip())) > 1)]

            name = " ".join(list(set([cur_tuple[0] for cur_tuple in sentence if cur_tuple[1] == 'PERSON'])))
            title = ""

            if bool(set(possible_title_words_1).intersection(set(real_title_words))) and len(possible_title_words_1) < 10:
                title = " ".join(possible_title_words_1)

            elif bool(set(possible_title_words_2).intersection(set(real_title_words))) and len(possible_title_words_2) < 10:
                title = " ".join(possible_title_words_2)

            elif bool(set(possible_title_words_3).intersection(set(real_title_words))) and len(possible_title_words_3) < 10:
                title = " ".join(possible_title_words_3)

            entity = {'name': name, 'title': title}
            if entity not in personsList:
                personsList.append(entity)

    return personsList