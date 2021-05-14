"""Test file to test code before it is implemented into assignment. Mianly to make sure that nothing breaks before
I mess with my data"""
import spacy
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import tqdm
from collections import Counter
import operator


nlp = spacy.load("en_core_web_sm") # might need to use large?

scraped_data = pd.read_csv("scraped_info.csv")

scraped_data = scraped_data[["Title of Post", "Post Description"]]

scraped_data["Title of Post"] = scraped_data["Title of Post"].str.encode("ascii", "ignore").str.decode("ascii")
scraped_data["Post Description"] = scraped_data["Post Description"].str.encode("ascii", "ignore").str.decode("ascii")


titles = scraped_data["Title of Post"]
titles = titles.tolist()

descriptions = scraped_data["Post Description"]
descriptions = descriptions.tolist()

for i in range(1,20):


    words = word_tokenize(titles[i])
    print(words)

    pos_tags = pos_tag(words)
    pos_tags_first = pos_tags[0]
    print(pos_tags)

    named_entities = ne_chunk(pos_tag(words))
    print(named_entities)










organisations_titles = []

for title in tqdm.tqdm(titles):
    try:
        title_raw = nlp(title)
        for word in title_raw.ents:
            if word.label_ == "ORG":
                organisations_titles.append(word.text)
    except:
        pass

print("titles")
top_organisations_titles = Counter(organisations_titles)
top_organisations_titles_ordered = sorted(top_organisations_titles.items(), key=operator.itemgetter(1), reverse=True)
print(top_organisations_titles_ordered)




# descriptions = scraped_data["Post Description"]
# descriptions = descriptions.tolist()
organisations_descriptions = []


for description in tqdm.tqdm(descriptions):
    try:
        #print("new description")
        description_raw = nlp(description)
        for word in description_raw.ents:
            if word.label_ == "ORG":
                organisations_descriptions.append(word.text)
            #print(word.text, word.label_)
    except:
        pass

print("descriptions")
top_organisations_descriptions = Counter(organisations_descriptions)
top_organisations_descriptions_ordered = sorted(top_organisations_descriptions.items(), key=operator.itemgetter(1), reverse=True)
print(top_organisations_descriptions_ordered)








