from scrapeModule import *
from ofstedScrape import *
s = scraper()
run = ofstedPostCodeRank(url="https://reports.ofsted.gov.uk/search?q=&location=&lat=&lon=&radius=&latest_report_date_start=&latest_report_date_end=&status[]=1&level_1_types=1&start=0&rows=14000&level_2_types[]=1&level_2_types[]=2")
if __name__ == "__main__":
    print("""ZOOPLA SCRAPER V 0.1""")
    print("\n")
    print("Option 1 : Postcode district scraper(gets titles, links and price)")
    print("Option 2 : OfstedScraper")
    print("\n")
    UserInput = str(input("Enter option  :  "))
    if UserInput == "1":
        s.Scrape()
    elif UserInput == "2":
        run.fetch()
        run.parse()
        run.ranker()
    else:
        print("Invalid option")
        time.sleep(1)
        quit()