"""File to extract the most common nouns and verbs"""

import spacy
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
import tqdm
from collections import Counter
import operator
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


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

def lemmatise_dataset(dataset):
    for i in range(len(dataset)):
        current_description = dataset.iloc[i]["Post Description"]
        word_list = nltk.word_tokenize(current_description)
        lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
        dataset.iloc[i]["Post Description"] = lemmatized_output

        return dataset






# add common car terms to stop words list as they do nor provide information on part failures
stop_words.add('car')
stop_words.add('problem')
stop_words.add('issue')
stop_words.add("Thanks")

top_dataframe = pd.read_csv("Top brand.csv")
second_dataframe = pd.read_csv("Second brand.csv")
third_dataframe = pd.read_csv("Third brand.csv")
fourth_dataframe = pd.read_csv("Fourth brand.csv")
fifth_dataframe = pd.read_csv("Fifth brand.csv")


top_dataframe = remove_stop_words(top_dataframe)
top_dataframe = lemmatise_dataset(top_dataframe)

second_dataframe = remove_stop_words(second_dataframe)
second_dataframe = lemmatise_dataset(second_dataframe)

third_dataframe = remove_stop_words(third_dataframe)
third_dataframe = lemmatise_dataset(third_dataframe)

fourth_dataframe = remove_stop_words(fourth_dataframe)
fourth_dataframe = lemmatise_dataset(fourth_dataframe)

fifth_dataframe = remove_stop_words(fifth_dataframe)
fifth_dataframe = lemmatise_dataset(fifth_dataframe)





descriptions = top_dataframe["Post Description"]
descriptions = descriptions.tolist()
top_nouns = []

for description in tqdm.tqdm(descriptions):
    words = nlp(description)
    for word in words:
        # print(word.text, word.pos_)
        if word.pos_ == "NOUN":
            top_nouns.append(word.text)
print(top_nouns)
top_nouns_found = Counter(top_nouns)
top_nouns_ordered = sorted(top_nouns_found.items(), key=operator.itemgetter(1), reverse=True)
top_nouns_ordered = top_nouns_ordered[0:5]
print(top_nouns_ordered)
