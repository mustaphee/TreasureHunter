#! usr/bin/python3
#Author: Mustapha Yusuff
#Email: officialwebdev@gmail.com

import requests
from bs4 import BeautifulSoup as b




base_url = 'https://www.jumia.com.ng/fitness/'

def csv_writer(name, price, url):
  with open('products.csv', 'a') as f:
    f.write(name + ',' + price + ',' + url + ','+ '\n')
    f.close()

def txt_writer(allProducts):
    with open('products.txt','a') as f:
        f.write(allProducts)
        f.close()


def get_details(soup):	
  pepper_soup = soup.find_all('div', {'class': 'sku -gallery'})
  print('Getting all products, and keeping my eyes peeled for the Treasure :p')

  for chilli in pepper_soup:
    
    name = chilli.find('span', {'class': 'name'}).get_text()
    price = chilli.find('span', {'class': 'price '}).find('span', {'dir': 'ltr'})['data-price']
    url = chilli.find('a', attrs={"class": "link"})['href']
    total_products =+ 1
    if price == '500': 
        print('\n'+"Found a Suspect, check "+name+" It is sold for "+price+" The url is "+url)
        output = (("*"*95)+'\n'+"This Might be the Product we are looking for!!!"+"\n"+"Product Name: "+name+ "\n" +"Product Price: "+price+"\n"+"Product Link: "+url+"\n"+("*"*95)+'\n')
    else:
        output = ("Product Name: "+name+ "\n" +"Product Price: "+price+"\n"+"Product Link: "+url+"\n"+("=="*30)+"\n")
    csv_writer(name, price, url)
    txt_writer(output)



def get_page_content(url):

  with requests.get(url) as response:
    page_soup = b(response.content, 'html.parser')
    print('\n'+"Gotcha Jumia, let's look for more page in this category")
    try:
        next_page = page_soup.find('a', attrs={'title': 'Next'})['href']
        parent_container = page_soup.find('section', {'class': 'products -mabaya'}) 
        print(next_page)
        get_details(parent_container)
        if next_page:
            get_page_content(next_page)
    
    except TypeError:
        print("Opps... An Error has occured!!!"+"\n"+"Relax, no Red Page, just that you have reached the end of the pages in this category!")

def main():
    print("Ready to get some goodies, shall we?")
    get_page_content(base_url)

if __name__ == '__main__':
  main()