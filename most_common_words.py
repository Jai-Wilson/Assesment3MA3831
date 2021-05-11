
import operator
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def get_top_words(input_string):

    top_words = Counter(input_string)
    top_words_ordered = sorted(top_words.items(),key=operator.itemgetter(1),reverse=True)
    print(top_words_ordered)
    top_twenty = top_words_ordered[0:20]
    print(top_twenty)
    return top_twenty

def remove_stop_words(input_string):
    filtered_words = []

    for word in input_string:
        if word not in stop_words:
            filtered_words.append(word)
    print(filtered_words)
    return filtered_words

def plot_most_common_words(plotting_string):
    top_twenty_after_stop = get_top_words(plotting_string)
    top_twenty_after_stop_dict = dict(top_twenty_after_stop)
    keys = top_twenty_after_stop_dict.keys()
    top_twenty_after_stop = get_top_words(plotting_string)
    top_twenty_after_stop_dict =dict(top_twenty_after_stop)
    keys = top_twenty_after_stop_dict.keys()
    values = top_twenty_after_stop_dict.values()
    plt.bar(keys, values)
    plt.xticks(rotation = 75)
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
titles = titles.tolist()
titles_string = ""
for i in range(len(titles)):
    title = titles[i]
    try:
        titles_string = titles_string + title + " "
    except:
        pass
titles_string = titles_string.split()

top_twenty = get_top_words(titles_string)

#remove stop words
stop_words = set(stopwords.words('english'))

filtered_titles = remove_stop_words(titles_string)

plot_most_common_words(filtered_titles)














