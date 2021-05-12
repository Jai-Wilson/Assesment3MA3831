organisations_titles = []

for title in tqdm.tqdm(titles):
    try:
        title_raw = nlp(title)
        for word in title_raw.ents:
            if word.label_ == "ORG":
                organisations_titles.append(word.text)
    except:
        pass