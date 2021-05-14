"""File that scrapes the Eric the Car guy. The specific page that is scraped is a service and repairs forum.
This forum and page was chosen as this page will mention specifc car brands, models, hat part is failing and
verbs associated with the parts that are failing."""

import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import tqdm

general_url = "https://www.ericthecarguy.com/forums/forum/stay-dirty-lounge/service-and-repair-questions-answered-here/"

filename = "scraped_info.csv"
f = open(filename, "a")

headers = "Date Posted,Author,Title of Post,Post Description\n"

f.write(headers)

# got to page 501

for j in tqdm.tqdm(range(501, 531)):
    print("Up to page {}".format(j))
    if j != 1:
        current_url = general_url + "page/" + "{}".format(j) + "/"
    else:
        current_url = general_url

    for i in range(0, 15):

        try:
            # opening connection, grabbing the page
            uClient = uReq(current_url)
            page_html = uClient.read()
            uClient.close()

            # html parsing
            page_soup = soup(page_html, "html.parser")

            # grabs each topic
            # find all where class is bhp-body
            containers = page_soup.findAll("li", {"class": "bbp-topic-title"})
            # inspect each container
            # inspect the a tag
            container = containers[i + 1]  # this is indexed depending on the article
            new_url = container.a['href']
            # get the url that references what the user has said

            person_posted = page_soup.findAll("span", {"class": "bbp-topic-started-by"})
            author_name = person_posted[i].a.img["alt"]  # indexed depending on the article

            # opening connection, grabbing the page
            uClient = uReq(new_url)
            new_page_html = uClient.read()
            uClient.close()
            new_page_soup = soup(new_page_html, "html.parser")
            # extract the title
            forum_title = new_page_soup.h1.span.text

            # extract the article description
            new_containers = new_page_soup.findAll("div", {"class": "bbp-topic-content"})
            # text is contained in p tags
            text = new_containers[1].find_all('p')

            description = ""
            for i in range(len(text)):
                # extracts the raw text from the tag
                current_decription = text[i].text
                description = description + current_decription

            date_container = new_page_soup.findAll("span", {"class": "bbp-topic-post-date"})
            date_posted = date_container[0].text
        except:
            pass

        # some dickhead decided to post url's, this is so annoying, do a try catch and if it catches just pass it
        try:

            date_posted = date_posted.replace(", ", " ")

            forum_title = forum_title.replace(",", " ")
            forum_title = forum_title.replace("  ", " ")

            description = description.replace("\r\n", " ")
            description = description.replace(",", " ")
            description = description.replace("  ", " ")
            description = description.replace("\n", "")

            f.write(date_posted.replace(",", " ") + "," + author_name + "," + forum_title.replace(",", " ") + "," +
                    description + "\n")
        except:
            pass

f.close()
