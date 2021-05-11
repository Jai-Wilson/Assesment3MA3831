import spacy
import pandas as pd
from spacy import displacy
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import tqdm
nlp = spacy.load("en_core_web_sm") # might need to use large?

scraped_data = pd.read_csv("scraped_info.csv")

scraped_data = scraped_data[["Title of Post", "Post Description"]]

scraped_data["Title of Post"] = scraped_data["Title of Post"].str.encode("ascii", "ignore").str.decode("ascii")
scraped_data["Post Description"] = scraped_data["Post Description"].str.encode("ascii", "ignore").str.decode("ascii")

# change everything in dataframe to lowercase
#scraped_data["Title of Post"] = scraped_data["Title of Post"].str.lower()
#scraped_data["Post Description"] = scraped_data["Post Description"].str.lower()

titles = scraped_data["Title of Post"]
titles = titles.tolist()

descriptions = scraped_data["Post Description"]
descriptions = descriptions.tolist()

print(titles[0])
print(descriptions[0])

words = word_tokenize(titles[0])
print(words)

pos_tags = pos_tag(words)
print(pos_tags)

named_entities = ne_chunk(pos_tags)
print(named_entities)


title_raw = nlp(titles[0])
print(title_raw.ents)
for word in title_raw.ents:
    # the label is stored as a string, organisation is "ORG"
    label = word.label_
    print(word.text, word.label_)

# descriptions = scraped_data["Post Description"]
# descriptions = descriptions.tolist()
organisations = []


for description in tqdm.tqdm(descriptions):
    try:
        #print("new description")
        description_raw = nlp(description)
        for word in description_raw.ents:
            if word.label_ == "ORG":
                organisations.append(word.text)
            #print(word.text, word.label_)
    except:
        pass

print(organisations)








