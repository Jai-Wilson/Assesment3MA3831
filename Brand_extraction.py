"""This file extracts the top 5 most mentioned organisations recognised using named entity reocgnition. Of these
extracted blog posts, it then puts data into 5 different dataframes. Each dataframe contains only posts specific
to that brand of car. Overall, the end product is 5 dataframes/csv files that contains posts relevant ot the top 5
extracted entities (car brands)"""

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
            if word.label_ == "ORG":
                organisations_titles.append(word.text)
    except:
        pass

print("titles")
top_organisations_titles = Counter(organisations_titles)
top_organisations_titles_ordered = sorted(top_organisations_titles.items(), key=operator.itemgetter(1), reverse=True)
top_ten_organisations = top_organisations_titles_ordered[0:5]
print(top_ten_organisations)

top_organisations_dict = dict(top_ten_organisations)

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

column_names = ["Title of Post", "Post Description"]

filtered_data_first = pd.DataFrame(columns=column_names)
filtered_data_second = pd.DataFrame(columns=column_names)
filtered_data_third = pd.DataFrame(columns=column_names)
filtered_data_fourth = pd.DataFrame(columns=column_names)
filtered_data_fifth = pd.DataFrame(columns=column_names)

for organisation in tqdm.tqdm(organisations_list):
    try:
        for i in range(len(scraped_data)):
            post = scraped_data.iloc[i]
            if organisation in post["Title of Post"]:
                if organisation == organisations_list[0]:
                    filtered_data_first = filtered_data_first.append(
                        {"Title of Post": post["Title of Post"], "Post Description": post["Post Description"]},
                        ignore_index=True)
                elif organisation == organisations_list[1]:
                    filtered_data_second = filtered_data_second.append(
                        {"Title of Post": post["Title of Post"], "Post Description": post["Post Description"]},
                        ignore_index=True)
                elif organisation == organisations_list[2]:
                    filtered_data_third = filtered_data_third.append(
                        {"Title of Post": post["Title of Post"], "Post Description": post["Post Description"]},
                        ignore_index=True)
                elif organisation == organisations_list[3]:
                    filtered_data_fourth = filtered_data_fourth.append(
                        {"Title of Post": post["Title of Post"], "Post Description": post["Post Description"]},
                        ignore_index=True)
                elif organisation == organisations_list[4]:
                    filtered_data_fifth = filtered_data_fifth.append(
                        {"Title of Post": post["Title of Post"], "Post Description": post["Post Description"]},
                        ignore_index=True)

    except:
        pass

filtered_data_first.to_csv("Top brand.csv", index=False)
filtered_data_second.to_csv("Second brand.csv", index=False)
filtered_data_third.to_csv("Third brand.csv", index=False)
filtered_data_fourth.to_csv("Fourth brand.csv", index=False)
filtered_data_fifth.to_csv("Fifth brand.csv", index=False)

print("Finished successfully")
