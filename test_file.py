"""Test file to test code before it is implemented into assignment. Mianly to make sure that nothing breaks before
I mess with my data"""


import spacy
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import tqdm
from collections import Counter
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nlp = spacy.load("en_core_web_sm")
# might need to use large?

scraped_data = pd.read_csv("example.csv")

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
            if word.label_ == "ORG":
                organisations_titles.append(word.text)
    except:
        pass

print("titles")
top_organisations_titles = Counter(organisations_titles)
top_organisations_titles_ordered = sorted(top_organisations_titles.items(), key=operator.itemgetter(1), reverse=True)
top_five_organisations = top_organisations_titles_ordered[0:5]
print(top_five_organisations)

top_organisations_dict = dict(top_five_organisations)

# extract the most common brands as a list
organisations_list = list(top_organisations_dict.keys())

top_ten_keys = top_organisations_dict.keys()
values = top_organisations_dict.values()
plt.bar(top_ten_keys, values)
plt.xticks(rotation=75)
plt.xlabel("Most commonly recognised entities")
plt.ylabel("Frequency")
plt.title("Most common entities recognised in scraped database")
plt.show()



















