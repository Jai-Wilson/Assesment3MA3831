"""File to extract the most common nouns and verbs"""

import spacy
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
import tqdm
from collections import Counter
import operator
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))


def remove_stop_words(dataset):
    for i in range(len(dataset)):
        current_description = dataset.iloc[i]["Post Description"]

        tokenised_description = word_tokenize(current_description)
        filtered_description = []

        for word in tokenised_description:
            if word not in stop_words:
                filtered_description.append(word)
        new_description = " ".join(filtered_description)

        dataset.iloc[i]["Post Description"] = new_description

    return dataset


# add common car terms to stop words list as they do nor provide information on part failures





top_dataframe = pd.read_csv("Top brand.csv")
second_dataframe = pd.read_csv("Second brand.csv")
third_dataframe = pd.read_csv("Third brand.csv")
fourth_dataframe = pd.read_csv("Fourth brand.csv")
fifth_dataframe = pd.read_csv("Fifth brand.csv")

print(top_dataframe)
print("removed stopwords")
top_dataframe = remove_stop_words(top_dataframe)
print(top_dataframe)
print(second_dataframe)
print(third_dataframe)
print(fourth_dataframe)
print(fifth_dataframe)

descriptions = top_dataframe["Post Description"]
descriptions = descriptions.tolist()
top_nouns = []

for description in tqdm.tqdm(descriptions):
    words = nlp(description)
    for word in words:
        #print(word.text, word.pos_)
        if word.pos_ == "NOUN":
            top_nouns.append(word.text)
print(top_nouns)
top_nouns_found = Counter(top_nouns)
top_nouns_ordered = sorted(top_nouns_found.items(), key=operator.itemgetter(1), reverse=True)
top__nouns_ordered = top_nouns_ordered[0:5]
print(top_nouns_ordered)



