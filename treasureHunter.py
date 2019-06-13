#! usr/bin/python3
#Author: Mustapha Yusuff
#Email: officialwebdev@gmail.com

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import sys


def csv_writer(name, price, url):
  with open('products.csv', 'a') as file:
    file.write(name + ',' + price + ',' + url + ','+ '\n')
    file.close()

def txt_writer(allProducts):
    with open('products.txt','a') as f:
        file.write(allProducts)
        file.close()

def json_writer(resp):
    with open('products.json', 'a') as file:
        file.write(json.dumps(resp, indent = 4))
        file.close()


def get_details(soup):
  pepper_soup = soup.find('section', {'class': 'products -mabaya'})
  name = pepper_soup.find_all('span', class_="name")
  price = pepper_soup.select('[class="price"]')
  url = pepper_soup.find_all('a', class_="link")

  return [{'name': each[0].get_text(), 
        'price': each[1].find('span', {'dir': 'ltr'}).get_text(),
        'url': each[2]['href']} for each in zip(name, price, url)]

def treasurer(soup):
    for product in get_details(soup):
        if product.price < 600:
            print('\n'+"Found a Suspect, check "+product.name+" It is sold for "+product.price+" The url is "+product.url)
            output = (("*"*95)+'\n'+"This Might be the Product we are looking for!!!"+"\n"
                +"Product Name: "+product.name+ "\n" +"Product Price: "+product.price+"\n"+"Product Link: "+product.url+"\n"+("*"*95)+'\n')
        else:
            output = ("Product Name: "+product.name+ "\n" +"Product Price: "+product.price+"\n"+"Product Link: "+product.url+"\n"+("=="*30)+"\n")
            csv_writer(product.name, product.price, product.url)
            txt_writer(output)
            json_writer(get_details)

# def get_details(soup):	
#   pepper_soup = soup.find_all('div', {'class': 'sku -gallery'})
#   print('Getting all products, and keeping my eyes peeled for the Treasure :p')

#   for chilli in pepper_soup:
    
#     name = chilli.find('span', {'class': 'name'}).get_text()
#     price = chilli.find('span', {'class': 'price '}).find('span', {'dir': 'ltr'})['data-price']
#     url = chilli.find('a', attrs={"class": "link"})['href']
#     total_products =+ 1
#     if price == '500': 
#         print('\n'+"Found a Suspect, check "+name+" It is sold for "+price+" The url is "+url)
#         output = (("*"*95)+'\n'+"This Might be the Product we are looking for!!!"+"\n"+"Product Name: "+name+ "\n" +"Product Price: "+price+"\n"+"Product Link: "+url+"\n"+("*"*95)+'\n')
#     else:
#         output = ("Product Name: "+name+ "\n" +"Product Price: "+price+"\n"+"Product Link: "+url+"\n"+("=="*30)+"\n")
#     csv_writer(name, price, url)
#     txt_writer(output)



def get_page_content(url):
    try:
        response = requests.get(url)
        page_soup = BeautifulSoup(response.content, 'lxml')
        print('\n'+"Gotcha Jumia, let's look for more page in this category")
        try:
            treasurer(soup)
            next_page_url = page_soup.find('a', attrs={'title': 'Next'})['href']
            if next_page:
                get_page_content(next_page_url)
        
        except TypeError:
            print("Opps... An Error has occured!!!"+"\n"+"Relax, no Red Page, just that you have reached the end of the pages in this category!")

    except ConnectionError:    
            print('Uh, ho. Your Internet just threw up...!!! Hanging Up now.')
            sys.exit(0)

def main(url):
    print("Ready to get some goodies, shall we?")
    get_page_content(url)

if __name__ == '__main__':
    if len(sys.argv) < 2:
       print('You did not pass in a category url as an argument. Scraper will exit now...')
       sys.exit(0) 
    else:
        url = sys.argv[1]
        main(url)