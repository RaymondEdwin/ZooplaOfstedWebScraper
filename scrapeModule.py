import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import random
import json
import datetime
class scraper:
    def __init__(self):
        pass
    def Scrape(self):


        titles = []
        urls = []
        postCodeList = ("N9","W10","N1")
        for postCode in postCodeList:
            for page in range(1, 3):
                url = (
                    str(f"https://www.zoopla.co.uk/for-sale/property/{postCode}/?page_size=500&view_type=list&q=&radius=0&results_sort=newest_listings&search_source=refine&pn={page}"))
                urls.append(url)
        with open("proxies.txt","r") as f:
            proxiestxt = f.read()
        f.close
        proxiestxt = proxiestxt.replace(" ","")
        proxies = proxiestxt.split("\n")
        LinkList = []
        PriceList = []
        title_list = []
        LocationList = []
        NewLocationList = []

        def transform(url):
            randInt = random.randint(1, len(proxies))
            IP = proxies[randInt]
            IPs = f"http://{IP}"
            Proxy = {
                "http": IPs
            }
            r = requests.get(str(url), proxies=Proxy).text
            soup = BeautifulSoup(r, 'html.parser')

            for link in soup.find_all("a", "e2uk8e20 css-1rzeb2c-StyledLink-Link-StyledLink e33dvwd0"):
                y1 = (link.get("href"))
                x = (f"https://www.zoopla.co.uk{y1}")
                LinkList.append(x)
            for link in soup.find_all("p", "css-1o565rw-Text eczcs4p0"):
                link = str(link)
                link = link.replace("""<p class=\"css-1o565rw-Text eczcs4p0\" size=\"6\">""", "")
                link = link.replace("</p>", "")
                x = (link)
                x = x.replace("£", "")
                x = x.replace(",", "")
                PriceList.append(x)
            for link in soup.find_all("h2", "css-vthwmi-Heading2-StyledAddress e2uk8e16"):
                y1 = str(link)
                y1 = y1.replace("listing-title\" size=\"8\">", "----")
                y1 = y1.replace("</h2>", "----")
                y1 = y1.split("----")
                x = (y1[1])
                title_list.append(x)
            Grids = soup.find_all("p", class_="css-nwapgq-Text eczcs4p0")
            Length = len(Grids)
            Lists = []
            for i in range(0, Length):
                if "listing-description" in str(Grids[i]):
                    x=str(Grids[i])
                    x=x.replace("<p class=\"css-nwapgq-Text eczcs4p0\" data-testid=\"listing-description\">","")
                    x=x.replace("</p>","")
                    x=x.replace(",","")
                    LocationList.append(x)
                else:
                    pass




            print(url)
            return

        pre = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=350) as executor:
            executor.map(transform, urls)

        _time = (time.time() - pre)


        Length__ = len(LinkList)
        print(f"{(float(Length__) / (_time) * 60)} CPM")





        HEADERS = "Title,Price,Location,Link"
        with open (f"Results/ZooplaDB_{pre}.csv","w") as f:
            f.write(HEADERS)
            f.write("\n")
        f.close()

        for i in range(len(LinkList)):
            STRING = (f"{title_list[i]},{PriceList[i]},{LocationList[i]},{LinkList[i]}")
            print(STRING)
            with open(f"Results/ZooplaDB_{pre}.csv", "a") as f:
                f.write(STRING)
                f.write("\n")
            f.close()
        print(_time)
        print(len(LinkList))
        print(len(title_list))
        print(len(PriceList))
        print(len(LocationList))
        print(len(LinkList)/(_time)*60)