"""File to extract the most common  words that appeared in the database after stop word removal for data exploration
purposes, and to allow a user to undertsand the data better."""

import operator
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import string


def get_top_words(input_string):
    """A function to count the most common words in a string"""
    # count the words
    top_words = Counter(input_string)
    # order the words in descending order
    top_words_ordered = sorted(top_words.items(), key=operator.itemgetter(1), reverse=True)
    # keep the top twenty elements
    top_twenty = top_words_ordered[0:20]
    print(top_twenty)
    return top_twenty


def listToString(s):
    """A function to turn a list to string. normally the .join function can be used, but
    catching erros in this was difficult, so this function is made"""
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
    """Turn a column of a dataframe to a list"""
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
    """Remove stop words from a list"""
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


def plot_most_common_words(plotting_string, method):
    """Plot the most common words in a string"""
    top_twenty_after_stop = get_top_words(plotting_string)
    top_twenty_after_stop_dict = dict(top_twenty_after_stop)
    keys = top_twenty_after_stop_dict.keys()
    values = top_twenty_after_stop_dict.values()
    plt.bar(keys, values)
    plt.xticks(rotation=75)
    plt.xlabel("Most common words")
    plt.ylabel("Frequency")
    plt.title("Most common words in {} of posts from ErictheCarGuy".format(method))
    plt.show()


scraped_data = pd.read_csv("scraped_info.csv")

# keep the desired columns
scraped_data = scraped_data[["Title of Post", "Post Description"]]

# removes non UTF-8 encoding of any scraped information
scraped_data["Title of Post"] = scraped_data["Title of Post"].str.encode("ascii", "ignore").str.decode("ascii")
scraped_data["Post Description"] = scraped_data["Post Description"].str.encode("ascii", "ignore").str.decode("ascii")

# change everything in descriptions dataframe to lowercase. Don't change titles dataframe to lowercase as it will not
# be changed for NER analysis
scraped_data["Post Description"] = scraped_data["Post Description"].str.lower()

# extract titles
titles = scraped_data["Title of Post"]
titles_list = column_to_list(titles)

# extract descriptions
descriptions = scraped_data["Post Description"]
descriptions_list = column_to_list(descriptions)

# get the top 20 words for titles and descriptions
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

# remove stop words
scraped_data = remove_stop_words(scraped_data)
filtered_titles = scraped_data["Title of Post"]
filtered_titles = column_to_list(filtered_titles)
filtered_descriptions = scraped_data["Post Description"]
filtered_descriptions = column_to_list(filtered_descriptions)

# plot the most common words
plot_most_common_words(filtered_titles, "titles")
plot_most_common_words(filtered_descriptions, "descriptions")

desc_string = ""
for description in descriptions:
    try:
        desc_string = desc_string + " " + description
    except:
        pass
wc = WordCloud(background_color='white', height=400, width=600)
wc.generate(desc_string)
plt.imshow(wc)
plt.axis('off')
plt.show()
wc.to_file('wordcloud_descriptions.png')

title_string = ""
for title in titles:
    try:
        title_string = title_string + " " + title
    except:
        pass
wc = WordCloud(background_color='white', height=400, width=600)
wc.generate(title_string)
plt.imshow(wc)
plt.axis('off')
plt.show()
wc.to_file('wordcloud_titles.png')

