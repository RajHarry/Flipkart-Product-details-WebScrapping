from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests 
from collections import Counter

products,orig_price,off_price,off_perc,brands,f_as,products_link = [],[],[],[],[],[],[]

#1) product name
#2) product brand
#3) category

base = "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=relevance"
for i in range(3):
	query = input("Enter a query: ")
	def make_url(question):
		n1 = list(map(str,query.strip().split()))
		s1 = ""
		for i in range(len(n1)-1):
			s1 = s1+n1[i]+"%20"
		s1 = s1+n1[-1]

		s1 = "https://www.flipkart.com/search?q="+s1+base
		return s1
	URL = make_url(query)
	#print(URL)
	#continue
	#assert(False)
	r = requests.get(URL)
	soup = BeautifulSoup(r.content,'html5lib')

	for row in soup.findAll('a',href=True,attrs={'class':'_3dqZjq'}):
		products_link.append("https://www.flipkart.com"+row['href'])
	for num,row in enumerate(soup.findAll('div',attrs={'class':'_2LFGJH'})):
		product_name = row.find('a', href=True, attrs={'class':'_2mylT6'}).text
		products.append(product_name)
		brand = row.find('div', attrs={'class':'_2B_pmu'})
		try:
			brands.append(brand.text)
		except:
			brands.append("None")
		price=row.find('a', href=True, attrs={'class':'_2W-UZw'})
		
		orig_price.append(price.find('div',attrs={'class':'_1vC4OE'}).text[1:])
		try:
			off_price.append(price.find('div',attrs={'class':'_3auQ3N'}).text[1:])
		except:
			off_price.append("NO")
		try:
			off_perc.append(price.find('div',attrs={'class':'VGWI6T'}).text)
		except:
			off_perc.append("NO")
		fass=row.find('div', attrs={'class':'_3AqcXr'})
		if(fass==None):
			f_as.append("False")
		else:
			f_as.append("True")

#print(products_link)
#print(dict(Counter(products_link)))
#print(len(products),len(orig_price),len(off_price),len(off_perc),len(brands),len(f_as),len(products_link))
df = pd.DataFrame({'Product Name':products,'Original_price':orig_price,'Offer_price':off_price,'percentage':off_perc,'Brand':brands,'assurance':f_as,'products_link':products_link}) 
df.to_csv('products_search.csv', index=False, encoding='utf-8')