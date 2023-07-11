from bs4 import BeautifulSoup
import requests
import re

product = input("What product do you want to search for? ")
minPrice = input("What is the minium price you would like to search for? ")
MaxPrice = input("What is the maxium price you would like to search for? ")


url = f"https://www.newegg.com/p/pl?d={product}&N=4131"
page = requests.get(url).text
doc =BeautifulSoup(page, "html.parser")

NumOfPagesText = doc.find(class_="list-tool-pagination-text").strong
NumOfPages = int(str(NumOfPagesText).split("/")[-2].split(">")[-1][:-1])
print(NumOfPages)

itemsFound = {}

for page in range(1, NumOfPages+1):
    url = f"https://www.newegg.com/p/pl?d={product}&N=4131&page={page}"
    page = requests.get(url).text
    doc =BeautifulSoup(page, "html.parser")

    #this div is the div that contains the table with all the items
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    
    items = div.find_all(string=re.compile(product))

    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue
        link = parent['href']
        grandParent = item.find_parent(class_="item-container")
        if grandParent.find(class_="price-current").find("strong"): #reason included this was because if there was a deal going on it wouldnt have a strong tag under current price thus leading to an error
            price = grandParent.find(class_="price-current").strong.text
            price = int(price.replace(",",""))
            if price <= int(MaxPrice) and price >= int(minPrice):
                itemsFound[item] = {"price": price, "link": link}

sorted_items = sorted(itemsFound.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("---------------------------------------------------------------------")

