from bs4 import BeautifulSoup
import requests
import time
class ofstedPostCodeRank:

    def __init__(self,url):
        self.url = url


    def fetch(self):
        r=requests.get(self.url).text
        self.r = r
        print("Scraped")

    def parse(self):
        soup = BeautifulSoup((self.r),"html.parser")
        schoolGrids = soup.find_all("li",class_="search-result")
        f = open("postCodetoRating.csv", "a")
        for i in schoolGrids:
            name = i.find("h3",class_="search-result__title heading--main").text
            location = i.find("address",class_="search-result__address").text
            rating = i.find("div",class_="search-result__provider-rating")
            rating=str(rating)
            rating = rating.replace("<div class=\"search-result__provider-rating\"><p>Rating: <strong>","")
            rating = rating.replace("</strong></p></div>","")
            postcodeDistrict = (location.split(" "))
            postcodeDistrict = postcodeDistrict[-2]
            f.write(f"{postcodeDistrict} , {rating}")
            f.write("\n")
        f.close()
    def ranker(self):
        f = open("postcodeList.txt","r")
        postcodes = str(f.read())
        f.close()
        f = open("postCodetoRating.csv","r")
        postCodetoRating = f.read()
        f.close()
        postCodetoRating = postCodetoRating.split("\n")
        postcodeDistrictList = postcodes.split("\n")
        score = {}
        for i in postcodeDistrictList:
            print("_____________________________________________")
            GoodCount = postCodetoRating.count(f"{i} , Good")
            print(f"Good : {GoodCount}")
            OutstandingCount = postCodetoRating.count(f"{i} , Outstanding")
            print(f"Outstanding : {OutstandingCount}")
            InadequateCount = postCodetoRating.count(f"{i} , Inadequate")
            print(f"Inadequate : {InadequateCount}")
            SatisfactoryCount = postCodetoRating.count(f"{i} , Satisfactory")
            print(f"Satisfactory : {SatisfactoryCount}")
            ImprovementCount = postCodetoRating.count(f"{i} , Requires Improvement")
            print(f"Requires Improvement : {ImprovementCount}")
            try:
                GoodandAbove = ((GoodCount+OutstandingCount)/(GoodCount+OutstandingCount+ImprovementCount+InadequateCount+SatisfactoryCount))
                print(f"{GoodandAbove*100}% of {i} schools are good or outstanding")
                score[str(i)] = (GoodandAbove*100)
                print(f"{i} has {InadequateCount/(GoodCount+OutstandingCount+ImprovementCount+InadequateCount+SatisfactoryCount)*100}% inadequate count")
            except:
                print(f"No stats for {i}")
        print(score)