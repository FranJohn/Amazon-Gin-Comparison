#Complete (I wrote)
from bs4 import BeautifulSoup
import requests
import re


class GinCompare:
    def __init__(self, name, price, rating):
        self.name = name
        self.price = price
        self.rating = rating

    def writer(self):
        saver = [f"<name> {self.name} </name>, <price> {self.price} </price>, <rating> {self.rating} </rating>"]
        gin_file = open("gin_parameters.csv", "a")  # append mode
        gin_file.write(f"{saver}\n")
#        gin_file.write(f"{self.name}\n{self.price}\n{self.rating}\n")
        print(f"{self.name}\n{self.price}\n{self.rating}\n")
        gin_file.close()


def main(url):
    gin_file = open("gin_parameters.csv", "a")  # append mode
    webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11)', 'Accept-Language': 'en-US, en;q=0.5'})
    soup = BeautifulSoup(webpage.content, "lxml")    # finding name
 # Gin type
    try:
        title = soup.find("span", attrs={"id": "productTitle"})  # Product title is name of the html
        title_str = title.string.strip().replace(",", "")
    except AttributeError:
        title_str = "Error"
    print("Name = ", title_str)
#    gin_file.write(f"{title_str},")
# Gin Price
    try:
        price = soup.find("span", attrs={"id": "priceblock_ourprice"})  # Product title is name of the html
        price_str = price.string.strip().replace(",", "")
    except AttributeError:
        price_str = "Error"
    print("Price = ", price_str)
#    gin_file.write(f"{price_str},")
# Gin Rating
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
        except:
            rating = "NA"
    print("Rating = ", rating)
#    gin_file.write(f"{rating},\n")
    gin = GinCompare(name=title_str, price=price_str, rating=rating)
    gin.writer()
    gin_file.close()


if __name__ == '__main__':
    file = open("url.txt", "r")  # Urls for use
    for links in file.readlines():
        main(links)
    gins = open("gin_parameters.csv", "r")
    pattern_name = "<name.*?>.*?</name>"
    pattern_price = "<price.*?>.*?</price>"
    pattern_rating = "<rating.*?>.*?</rating>"
    i = 0
    name = [""]
    price = 30 # Upper price
    for line in gins:
        i = line.index(line)
        match_price = re.search(pattern_price, line, re.IGNORECASE)
        price_temp = match_price.group()
        price_temp = re.sub("<.*?>", "", price_temp)
        price_temp = re.sub("£", "", price_temp)
        match_name = re.search(pattern_name, line, re.IGNORECASE)
        name_temp = match_name.group()
        name_temp = re.sub("<.*?>", "", name_temp)
        #print(name)
        match_rating = re.search(pattern_rating, line, re.IGNORECASE)
        rating_temp = match_rating.group()
        rating_temp = re.sub("<.*?>", "", rating_temp)
        #print(rating)
        if float(price_temp) <= float(price):
            price = price_temp
            name = name_temp
            rating = rating_temp
        else:
            price = price
            name = name
            rating = rating
        # print(price)

    print(name)
    print(price)
    print(rating)