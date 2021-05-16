'''A simple document for storing code that may/may not be used for the NLP tasks. This document is not
intended to be run or to add more meaning to the task, but simply for my assistance'''

# descriptions = top_dataframe["Post Description"]
# descriptions = descriptions.tolist()
top_nouns = []

for i in range(0, 5):
    if i == 0:
        descriptions = top_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif i == 1:
        descriptions = second_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif i == 2:
        descriptions = third_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif i == 3:
        descriptions = fourth_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    elif i == 4:
        descriptions = fifth_dataframe["Post Description"]
        descriptions = descriptions.tolist()
    current_nouns = []
    for description in tqdm.tqdm(descriptions):
        words = nlp(description)
        for word in words:
            # print(word.text, word.pos_)
            if word.pos_ == "NOUN":
                current_nouns.append(word.text)
    top_nouns_found = Counter(current_nouns)
    top_nouns_ordered = sorted(top_nouns_found.items(), key=operator.itemgetter(1), reverse=True)
    top_nouns_ordered = top_nouns_ordered[0:5]
    print(top_nouns_ordered)
    top_nouns.append(top_nouns_ordered)

print(top_nouns)