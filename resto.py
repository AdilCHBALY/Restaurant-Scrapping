import requests
import json
import base64
from bs4 import BeautifulSoup 
import re
from uuid import uuid4

# MAIN WEBSITE TO GET ALL RESTAURANTS IN ALL MORROCAN CITIES
# url = "https://www.tripadvisor.com/Restaurants-g293730-Morocco.html"

# URL FOR ALL RESTAURANTS IN A CITY
# url='https://www.tripadvisor.com/Restaurants-g293734-Marrakech_Marrakech_Safi.html'
# response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
# soup = BeautifulSoup(response.text, 'html.parser')


def get_long_lat(url):
    # Extract latitude and longitude from URL using regular expressions
    pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
    match = re.search(pattern, url)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude,longitude
    else:
        return 0,0

#Get a Single Restaurant Data 
def get_restaurant_data(url):
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')      

    details_list=[]
    imgs=[]
    if soup.find('a',class_='dlMOJ') is not None:
        restaurant_pricing_rate = soup.find('a',class_='dlMOJ').text
    else :
        restaurant_pricing_rate = 'N/A'
    if soup.find('h1',class_='HjBfq') is not None:
        restaurant_name = soup.find('h1',class_='HjBfq').text
    else : 
        restaurant_name = 'N/A'
    print("Fetching Restaurant : "+restaurant_name)
    if soup.find('span',class_='AfQtZ') is not None :
        review = soup.find('span',class_='AfQtZ').text
    else :
        review ='N/A'
    if  soup.find('span',class_='ZDEqb') is not None : 
        rating =soup.find('span',class_='ZDEqb').text
    else : 
        rating = 'N/A'
    details=soup.find_all('div',class_='SrqKb')
    if details :
        for detail in details : 
            details_list.append(detail.text)
    while len(details_list) < 3 :
        details_list.append('N/A')
    if soup.find('span',class_='yEWoV') is not None :
        address=soup.find('span',class_='yEWoV').text
    else :
        address = 'N/A'
    if soup.find('span',class_='mMkhr') : 
        status=soup.find('span',class_='mMkhr').text
    else :
        status = 'N/A'
    if soup.find('span',class_='AYHFM') :
        phone=soup.find('span',class_='AYHFM').text
    else : 
        phone='N/A'
    images = soup.find_all('img',class_='basicImg')
    if images is not None :
        for image in images :
            imgs.append(image['data-lazyurl'])
    #Decode the Encoded Url that google map provide
    if soup.find('a',class_='YnKZo Ci Wc _S C FPPgD') is not None:
        encoded_str = soup.find('a',class_='YnKZo Ci Wc _S C FPPgD')['data-encoded-url']
        decoded_str = base64.b64decode(encoded_str).decode('utf-8')
    else : 
        decoded_str = 'N/A'
    
    lat,long=get_long_lat(decoded_str[4:])

    restaurant_details = {
        'id':str(uuid4()),
        'name': restaurant_name,
        'review' : review,
        'rating' : rating,
        'img':imgs,
        'long':long,
        'lat':lat,
        'pricing' : restaurant_pricing_rate,
        'details' : details_list,
        'address':address,
        'status':status,
        'phone':phone
    }
    return restaurant_details


    

    
#This is to Fetch the Top 30 Restaurants in a City
def fetch_single_page(url):
    all_city_restaurant = []
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    restaurants = soup.find_all('div',class_='_T')
    for r in restaurants:
        if r.find('a',class_='aWhIG _S ygNMs Vt u Gi') is not None : 
            single_restaurant_link = "https://www.tripadvisor.com"+r.find('a',class_='aWhIG _S ygNMs Vt u Gi')['href']
            single_restaurant = {}
            single_restaurant = get_restaurant_data(single_restaurant_link)
            all_city_restaurant.append(single_restaurant)
    #You can add 60-90-120 Restaurant By Removing this code and adding a for loop for it 
    #url = "https://www.tripadvisor.com"+soup.find('a',class_="nav next rndBtn ui_button primary taLnk")['href']
    return all_city_restaurant
    



# #Get All the Restaurants Cities from the Website 
def get_restaurants():
    url = "https://www.tripadvisor.com/Restaurants-g293730-Morocco.html"
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    cities = soup.find_all('div', class_='geo_wrap')
    data = []
    i=1
    for city in cities:
        name = city.find('div', class_='geo_name')
        link = "https://www.tripadvisor.com"+name.find('a')['href']
        print("Fetching From " + name.text.strip())
        all_restaurants_data = fetch_single_page(link)
        restaurant_dict={
            'id':i,
            'name' : name.text.strip(),
            'restaurants':all_restaurants_data
        }
        data.append(restaurant_dict)
        i=i+1
    

    with open("./restaurants.json","w") as outfile :
        json.dump(data,outfile)
    
    print("File Saved Succefully")
    
get_restaurants()






