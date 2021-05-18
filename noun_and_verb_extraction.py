"""File to extract the most common nouns and verbs"""

import operator
from collections import Counter

import nltk
import pandas as pd
import spacy
import tqdm
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def merge_lists(list1, list2):
    combined_list = [(list1[n], list2[n]) for n in range(0, len(list1))]
    return combined_list


def remove_stop_words(dataset):
    for j in range(len(dataset)):
        current_description = dataset.iloc[j]["Post Description"]

        tokenised_description = word_tokenize(current_description)
        filtered_description = []

        for word in tokenised_description:
            if word not in stop_words:
                filtered_description.append(word)
        new_description = " ".join(filtered_description)

        dataset.iloc[j]["Post Description"] = new_description

    return dataset


def lemmatise_dataset(dataset):
    for i in range(len(dataset)):
        current_description = dataset.iloc[i]["Post Description"]
        word_list = nltk.word_tokenize(current_description)
        lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
        dataset.iloc[i]["Post Description"] = lemmatized_output

        return dataset


def get_descriptions(index):
    if index == 0:
        descriptions = top_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif index == 1:
        descriptions = second_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif index == 2:
        descriptions = third_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif index == 3:
        descriptions = fourth_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif index == 4:
        descriptions = fifth_dataframe["Post Description"]
        descriptions = descriptions.tolist()

    return descriptions


# add common car terms to stop words list as they do nor provide information on part failures
stop_words.add('car')
stop_words.add('problem')
stop_words.add('issue')
stop_words.add("Thanks")

# load in the dataframes from the csv files
top_dataframe = pd.read_csv("Top brand.csv")
second_dataframe = pd.read_csv("Second brand.csv")
third_dataframe = pd.read_csv("Third brand.csv")
fourth_dataframe = pd.read_csv("Fourth brand.csv")
fifth_dataframe = pd.read_csv("Fifth brand.csv")

# remove stop words and lemmatize the dataset
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

top_nouns = []

for i in range(0, 5):
    post_descriptions = get_descriptions(i)
    current_nouns = []
    for description in tqdm.tqdm(post_descriptions):
        words = nlp(description)
        for word in words:
            # print(word.text, word.pos_)
            if word.pos_ == "NOUN":
                current_nouns.append(word.text)
    top_nouns_found = Counter(current_nouns)
    top_nouns_ordered = sorted(top_nouns_found.items(), key=operator.itemgetter(1), reverse=True)
    top_nouns_ordered = top_nouns_ordered[0:5]
    # print(top_nouns_ordered)
    top_nouns.append(top_nouns_ordered)

# print the list vertically to be seen easier from the user

print(*top_nouns, sep="\n")

top_verbs = []

for i in range(0, 5):

    new_post_descriptions = get_descriptions(i)

    nouns = [new_tuple[0] for new_tuple in top_nouns[i]]  # nouns list needs to be changed here

    top_current_verbs = []
    for i in range(len(nouns)):
        current_verbs = []
        for description in new_post_descriptions:
            current_noun = nouns[i]
            # if noun is found in a description
            if current_noun in description:
                # split the description at the full stops to extract individual sentences of the description
                description = description.split(".")
                for sentence in description:
                    # if the noun is found in the sentence, find verbs, adverbs and adjectives in that sentence. These
                    # parts of speech are chosen as they will describe what is being talked about with that specific
                    # noun
                    if current_noun in sentence:
                        words = nlp(sentence)
                        for word in words:
                            if word.pos_ == "VERB" or word.pos_ == "ADV" or word.pos_ == "ADJ":
                                current_verbs.append(word.text)
        top_verbs_found = Counter(current_verbs)
        top_verbs_ordered = sorted(top_verbs_found.items(), key=operator.itemgetter(1), reverse=True)
        top_verb = top_verbs_ordered[0]
        top_current_verbs.append(top_verb)
    top_verbs.append(top_current_verbs)
print(*top_verbs, sep="\n")
# here, the top verb/describing word for each of the 5 nouns is found, as a list of 5 values. Append each of these lists
# to the top verbs list. So that the top verbs list contains 5 lists of verbs
top_nouns_and_verbs_found = []
for i in range(0, 5):
    nouns_list = [a_top_nouns[0] for a_top_nouns in top_nouns[i]]
    verbs_list = [a_top_verbs[0] for a_top_verbs in top_verbs[i]]
    merged_list = merge_lists(nouns_list, verbs_list)
    top_nouns_and_verbs_found.append(merged_list)
print(*top_nouns_and_verbs_found, sep="\n")
