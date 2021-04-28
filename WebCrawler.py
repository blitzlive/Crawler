import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv
# class muss immer mit .CLASSNAME geschrieben werden
# Was sind Generatoren? -> Schlüsselwort ist "yield" und wird benutzt, um keine extra Liste oder variable erzeugen zu müssen


class CrawledArticel():

    def __init__(self, title, emoji, content, image):
        self.title = title
        self.emoji = emoji
        self.content = content
        self.image = image


class ArticelFetcher():

    def fetch(self):
        url = "http://python.beispiel.programmierenlernen.io/index.php"
        articles = []

        while url != "":
            print(url)
            time.sleep(1)

            r = requests.get(url)
            # print(r.__dict__)
            # print(r.status_code)
            # print(r.headers)
            # print(r.text)
            doc = BeautifulSoup(r.text, "html.parser")

            for card in doc.select(".card"):
                emoji = card.select_one(".emoji").text
                content = card.select_one(".card-text").text
                title = card.select(".card-title span")[1].text
                imageOhneJoin = card.select_one("img").attrs["src"]
                image = urljoin(url, imageOhneJoin)
                crawled = CrawledArticel(title, emoji, content, image)
                articles.append(crawled)

            next_button = doc.select_one(".navigation .btn")
            if next_button:
                next_href = next_button.attrs["href"]
                next_link = urljoin(url, next_href)
            else:
                next_link = ""

            url = next_link

        return articles


def getWebsiteDataInCSV():
    fetcher = ArticelFetcher()
    with open("webcrawler.csv", "w", newline='') as csvfile:
        articlewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for article in fetcher.fetch():
            articlewriter.writerow([article.emoji, article.title, article.content, article.image])


getWebsiteDataInCSV()
