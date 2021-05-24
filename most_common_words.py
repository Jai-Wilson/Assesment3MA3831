"""File to extract the most common  words that appeared in the database after stop word removal for data exploration
purposes, and to allow a user to undertsand the data better."""

import operator
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from wordcloud import WordCloud
import string


def get_top_words(input_string):
    top_words = Counter(input_string)
    top_words_ordered = sorted(top_words.items(), key=operator.itemgetter(1), reverse=True)
    print(top_words_ordered)
    top_twenty = top_words_ordered[0:20]
    print(top_twenty)
    return top_twenty


# fix this function
# def remove_stop_words(input_string):
#     filtered_words = []
#
#     for word in input_string:
#         if word not in stop_words:
#             filtered_words.append(word)
#     print(filtered_words)
#     return filtered_words

def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        try:
            str1 = str1 + " " + ele
        except:
            pass

        # return string
    return str1


def column_to_list(column):
    column = column.tolist()
    column_string = ""
    for i in range(len(column)):
        current_row = column[i]
        try:
            column_string = column_string + current_row + " "
        except:
            pass
    column_list = column_string.split()
    return column_list


def remove_stop_words(dataset):
    for n in range(len(dataset)):
        try:
            # concatenate the title and keywords
            current_title = dataset.iloc[n]["Title of Post"]
            current_description = dataset.iloc[n]["Post Description"]

            token_title = word_tokenize(current_title)
            token_description = word_tokenize(current_description)
            filtered_title = []
            filtered_description = []

            for word in token_description:
                if word not in stop_words:
                    filtered_description.append(word)

            filtered_description = listToString(filtered_description)

            for word in token_title:
                if word not in stop_words:
                    filtered_title.append(word)

            filtered_title = listToString(filtered_title)

            dataset.iloc[n]["Title of Post"] = filtered_title
            dataset.iloc[n]["Post Description"] = filtered_description

        except:
            pass

    return dataset


def plot_most_common_words(plotting_string):
    top_twenty_after_stop = get_top_words(plotting_string)
    top_twenty_after_stop_dict = dict(top_twenty_after_stop)
    keys = top_twenty_after_stop_dict.keys()
    top_twenty_after_stop = get_top_words(plotting_string)
    top_twenty_after_stop_dict = dict(top_twenty_after_stop)
    keys = top_twenty_after_stop_dict.keys()
    values = top_twenty_after_stop_dict.values()
    plt.bar(keys, values)
    plt.xticks(rotation=75)
    plt.xlabel("Most common words")
    plt.ylabel("Frequency")
    plt.title("Most common words retrieved from ErictheCarGuy")
    plt.show()


scraped_data = pd.read_csv("scraped_info.csv")

scraped_data = scraped_data[["Title of Post", "Post Description"]]

# removes non UTF-8 encoding of any scraped information
scraped_data["Title of Post"] = scraped_data["Title of Post"].str.encode("ascii", "ignore").str.decode("ascii")
scraped_data["Post Description"] = scraped_data["Post Description"].str.encode("ascii", "ignore").str.decode("ascii")

# change everything in dataframe to lowercase
scraped_data["Title of Post"] = scraped_data["Title of Post"].str.lower()
scraped_data["Post Description"] = scraped_data["Post Description"].str.lower()

titles = scraped_data["Title of Post"]
titles_list = column_to_list(titles)
# titles = titles.tolist()
# titles_string = ""
# for i in range(len(titles)):
#     title = titles[i]
#     try:
#         titles_string = titles_string + title + " "
#     except:
#         pass
# titles_list = titles_string.split()

descriptions = scraped_data["Post Description"]
descriptions_list = column_to_list(descriptions)
# descriptions = descriptions.tolist()
# descriptions_string = ""
#
# for i in range(len(descriptions)):
#     description = descriptions[i]
#     try:
#         descriptions_string = descriptions_string + description + " "
#     except:
#         pass

# descriptions_list = descriptions_string.split()

top_twenty_titles = get_top_words(titles_list)
top_twenty_descriptions = get_top_words(descriptions_list)

# remove stop words
stop_words = set(stopwords.words('english'))
engl_alphabet = string.ascii_lowercase
engl_alphabet = list(engl_alphabet)
stop_words.update(engl_alphabet)
stop_words.add('.')
stop_words.add(',')
stop_words.add('?')
stop_words.add('(')
stop_words.add(')')
stop_words.add('!')
stop_words.add(':')

# filtered_titles = remove_stop_words(titles_string)
# filtered_descriptions = remove_stop_words(descriptions_string)


scraped_data = remove_stop_words(scraped_data)
filtered_titles = scraped_data["Title of Post"]
filtered_titles = column_to_list(filtered_titles)
filtered_descriptions = scraped_data["Post Description"]
filtered_descriptions = column_to_list(filtered_descriptions)


plot_most_common_words(filtered_titles)
plot_most_common_words(filtered_descriptions)

temp = ""
for description in descriptions:
    try:
        temp = temp + " " + description
    except:
        pass
print(temp)
wc = WordCloud(background_color='white', height=600, width=400)
wc.generate(temp)
wc.to_file('wordcloud_image.png')
