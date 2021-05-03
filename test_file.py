import pandas as pd

scraped_data = pd.read_csv("scraped_info.csv")
print(len(scraped_data))

scraped_data = scraped_data.drop_duplcates("Title of Post", keep = 'first', inplace = False)
print(len(scraped_data))