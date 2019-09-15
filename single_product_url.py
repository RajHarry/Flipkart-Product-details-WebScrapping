from bs4 import BeautifulSoup
import pandas as pd
import requests 

products,product_name,orig_price,off_price,off_perc,brands,f_as = [],[],[],[],[],[],[]
rating_points,ratings,reviews,price_list = [],[],[],[]
URL = "https://www.flipkart.com/apple-macbook-air-core-i5-5th-gen-8-gb-128-gb-ssd-mac-os-sierra-mqd32hn-a-a1466/p/itmevcpqqhf6azn3?pid=COMEVCPQBXBDFJ8C&srno=b_1_1&otracker=browse&lid=LSTCOMEVCPQBXBDFJ8C4V6AHG&fm=organic&iid=f5e7d991-7c35-461e-83c2-5bf79f8964a7.COMEVCPQBXBDFJ8C.SEARCH"
r = requests.get(URL)
soup = BeautifulSoup(r.content,'html5lib')

for row in soup.findAll('div',attrs={'class':'_29OxBi'}):
	#products.append(row.find('a', href=True, attrs={'class':'_35KyD6'}).text)
	product_name.append(row.find('span',attrs={'class':'_35KyD6'}).text)
	#brands.append(row.find('div', attrs={'class':'_2B_pmu'}).text)
	
	price = row.find('div', attrs={'class':'_3iZgFn'})
	orig_price.append(price.find('div',attrs={'class':'_1vC4OE _3qQ9m1'}).text[1:])
	try:
		off_price.append(price.find('div',attrs={'class':'_3auQ3N _1POkHg'}).text[1:])
	except:
		off_price.append("NO")
	try:
		off_perc.append(price.find('div',attrs={'class':'VGWI6T _1iCvwn'}).text)
	except:
		off_perc.append("NO")
	f2=row.find('div', attrs={'class':'niH0FQ _2nc08B'})
	#print(fass)
	rating_points.append(f2.find('div',attrs={'class':'hGSR34'}).text)
	f1 = row.find('span',attrs={'class':'_38sUEc'})
	for i in f1.find('span'):
		price_list.append((i.text).strip())
	#print(price_list)
	ratings.append(price_list[0].split(' ')[0])
	reviews.append(price_list[2].split(' ')[0])
	fass = row.find('span', attrs={'class':'_3V7-QV _55FW5e'})
	if(fass==None):
		f_as.append("False")
	else:
		f_as.append("True")
#print(len(product_name),len(orig_price),len(off_price),len(off_perc),len(f_as))
df = pd.DataFrame({'Product Name':product_name,'Original_price':orig_price,'Offer_price':off_price,'percentage':off_perc,'assurance':f_as}) 
df.to_csv('single_product_url.csv', index=False, encoding='utf-8')