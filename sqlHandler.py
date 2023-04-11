import mysql.connector
import json


mydb = mysql.connector.connect(
  user="root",
  password="energystar10",
  database="restaurant_recommendation"
)

mycursor = mydb.cursor()


def add_city(city_id,city_name):
  city_sql="INSERT INTO restaurant_recom_app_cities (id,city_name) VALUES (%s,%s)"
  city_val=(city_id,city_name)
  mycursor.execute(city_sql,city_val)
  mydb.commit()

def add_restaurant_detail(details):
  restaurant_detail_sql="INSERT INTO restaurant_recom_app_restaurant_details (montant,cuisine,top_food) VALUES (%s,%s,%s)"
  restaurant_detail_val=tuple(details)
  mycursor.execute(restaurant_detail_sql,restaurant_detail_val)
  mydb.commit()
  return mycursor.lastrowid

def add_restaurant(name,review,rating,long,lat,address,status,phone,city_id,restaurant_detail_id):
  restaurant_sql = "INSERT INTO restaurant_recom_app_restaurant ( name, review, rating, longt, lat, address, status, phone, city_id, restaurant_details_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  restaurant_val =(name,review,rating,long,lat,address,status,phone,city_id,restaurant_detail_id)
  print(restaurant_val)
  mycursor.execute(restaurant_sql,restaurant_val)
  mydb.commit()
  return mycursor.lastrowid

def add_restaurant_image(image,restaurant_id):
  image_sql = "INSERT INTO restaurant_recom_app_image (img_link,restaurant_id) VALUES (%s,%s)"
  image_val = (image,restaurant_id)
  mycursor.execute(image_sql,image_val)
  mydb.commit()



with open("./restaurants.json","r") as outfile :
  data = json.loads(outfile.read())

  for city in data : 
    restaurants = city['restaurants']
    city_id = city['id']
    city_name=city['name']
    add_city(city_id,city_name)
    for restaurant in restaurants:
      id = restaurant['id']
      name = restaurant['name']
      review = restaurant['review']
      rating = restaurant['rating']
      imgs = restaurant['img']
      long =str(restaurant['long'])
      lat = str(restaurant['lat'])
      pricing = restaurant['pricing']
      details = restaurant['details']
      detail_id=add_restaurant_detail(details)
      address=restaurant['address']
      status = restaurant['status']
      phone=restaurant['phone']
      restaurant_id=add_restaurant(name,review,rating,long,lat,address,status,phone,city_id,detail_id)
      for image in imgs :
        add_restaurant_image(image,restaurant_id)

