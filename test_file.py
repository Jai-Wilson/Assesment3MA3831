"""File that scrapes the Eric the Car guy. The specific page that is scraped is a service and repairs forum.
This forum and page was chosen as this page will mention specifc car brands, models, hat part is failing and
verbs associated with the parts that are failing."""

import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import tqdm

general_url = "https://www.ericthecarguy.com/forums/forum/stay-dirty-lounge/service-and-repair-questions-answered-here/"

filename = "example.csv"
f = open(filename, "w")

headers = "Date Posted,Author,Title of Post,Post Description\n"

f.write(headers)


# range of for loop is page start and page end
for j in tqdm.tqdm(range(1, 2)):
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
            # find all where class is bhp-topic-title
            containers = page_soup.findAll("li", {"class": "bbp-topic-title"})
            # inspect each container
            # inspect the a tag
            container = containers[i + 1]  # this is indexed depending on the article
            print(container)
            new_url = container.a['href']
            # get the url that references what the user has said
            print("new URL is {}".format(new_url))

            person_posted = page_soup.findAll("span", {"class": "bbp-topic-started-by"})
            print(person_posted)
            author_name = person_posted[i].a.img["alt"]  # indexed depending on the article
            print("The author of the post is {}".format(author_name))

            # opening connection, grabbing the page
            uClient = uReq(new_url)
            new_page_html = uClient.read()
            uClient.close()
            new_page_soup = soup(new_page_html, "html.parser")
            # extract the title
            forum_title = new_page_soup.h1.span.text
            print("Forum title is: {}".format(forum_title))

            # extract the article description
            new_containers = new_page_soup.findAll("div", {"class": "bbp-topic-content"})
            # text is contained in p tags
            text = new_containers[1].find_all('p')
            print("Raw description is: {}".format(text))

            description = ""
            for i in range(len(text)):
                # extracts the raw text from the tag
                current_decription = text[i].text
                description = description + current_decription

            date_container = new_page_soup.findAll("span", {"class": "bbp-topic-post-date"})
            print(date_container)
            date_posted = date_container[0].text
            print("Date posted is: {}".format(date_posted))
        except:
            pass

        # some users might post a url to another site, this causes the program to crash. If this occurs, simply pass
        # over the post and disregard it.
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