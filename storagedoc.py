'''A simple document for storing code that may/may not be used for the NLP tasks. This document is not
intended to be run or to add more meaning to the task, but simply for my assistance'''

import spacy
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import tqdm
from collections import Counter
import operator
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")
# might need to use large?

scraped_data = pd.read_csv("scraped_info.csv")

scraped_data = scraped_data[["Title of Post", "Post Description"]]

# remove any not-utf8 encoded characters
scraped_data["Title of Post"] = scraped_data["Title of Post"].str.encode("ascii", "ignore").str.decode("ascii")
scraped_data["Post Description"] = scraped_data["Post Description"].str.encode("ascii", "ignore").str.decode("ascii")

titles = scraped_data["Title of Post"]
titles = titles.tolist()

descriptions = scraped_data["Post Description"]
descriptions = descriptions.tolist()

organisations_titles = []

for title in tqdm.tqdm(titles):
    try:
        title_raw = nlp(title)
        for word in title_raw.ents:
            # print(word.text, word.label_)
            if word.label_ == "ORG":
                organisations_titles.append(word.text)
    except:
        pass
print("titles")
top_organisations_titles = Counter(organisations_titles)
top_organisations_titles_ordered = sorted(top_organisations_titles.items(), key=operator.itemgetter(1), reverse=True)
# top_ten_organisations = top_organisations_titles_ordered[0:5]
print(top_organisations_titles_ordered)
