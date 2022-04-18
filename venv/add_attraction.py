#packages imported
import numpy as np
import pandas as pd
import googlemaps
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#pull database from Cloud Firestore
db = firestore.client()

#method that presents the Add a Colorado Attraction page, which allows the user to add attractions to the list of
#Colorado Attractions that already are not on the list
def add_colorado_attraction():
    #imports the home_navigation_page method from the home_page.py file to allow the user access back to the home page
    from home_page import home_navigation_page

    #prints out the Add a Colorado Attraction header
    print("\nAdd a Colorado Attraction:")
    print("~~Before you add an attraction to the Colorado Attraction Database, please ensure that it is not already on the list~~\n")

    #prompt that asks the user to input the name of the attraction they would like to add
    new_attraction_name = input("Please type the name of the attraction you would like to add\n --> ")
    #prompt that asks the user to input the location of the attraction they would like to add
    new_attraction_location = input("In which city in Colorado is this attraction located?\n --> ")
    #prompt that asks the user to input the type of attraction that the attraction would like to add is from the given
    #categories
    new_attraction_type = input("Please type out what type of attraction your added attraction is from the following options: "
                                "Activity, Exhibit, Landmark, Mountains (For attractions that fit into multiple type of attraction "
                                "categories please separate the categories with a comma and a space) \n --> ")
    #prompt that asks the user to input if the attraction they would like to add has free parking
    new_attraction_free_parking = input("Does this attraction have free parking? (y/n)\n --> ")
    # prompt that asks the user to input if the attraction they would like to add has free WiFi
    new_attraction_free_wifi = input("Does this attraction have free WiFi? (y/n)\n --> ")
    # prompt that asks the user to input if the attraction they would like to add has a souvenir shop
    new_attraction_souvenir_shop = input("Does this attraction have a souvenir shop? (y/n)\n --> ")
    # prompt that asks the user to input if the attraction they would like to add is pet friendly
    new_attraction_pet_friendly = input("Is this attraction pet friendly? (y/n)\n --> ")

    #if the user indicates that the attraction that they would like to add has free parking, the new_attraction_free_parking
    #variable, which indicates if the added attraction has free parking, will be set to True
    if new_attraction_free_parking == "y":
        new_attraction_free_parking = True
    #if the user indicates that the attraction that they would like to add does not have free parking, the
    #new_attraction_free_parking variable, which indicates if the added attraction has free parking, will be set to False
    else:
        new_attraction_free_parking = False

    #if the user indicates that the attraction that they would like to add has free WiFi, the new_attraction_free_wifi
    #variable, which indicates if the added attraction has free WiFi, will be set to True
    if new_attraction_free_wifi == "y":
        new_attraction_free_wifi = True
    # if the user indicates that the attraction that they would like to add does not have free WiFi, the
    # new_attraction_free_wifi variable, which indicates if the added attraction has free wifi, will be set to False
    else:
        new_attraction_free_wifi = False

    #if the user indicates that the attraction that they would like to add has a souvenir shop, the
    #new_attraction_souvenir_shop variable, which indicates if the added attraction has a souvenir shop, will be set to True
    if new_attraction_souvenir_shop == "y":
        new_attraction_souvenir_shop = True
    # if the user indicates that the attraction that they would like to add does not have a souvenir shop, the
    # new_attraction_souvenir_shop variable, which indicates if the added attraction has a souvenir shop, will be set to False
    else:
        new_attraction_souvenir_shop = False

    # if the user indicates that the attraction that they would like to add is pet friendly, the
    # new_attraction_pet_friendly variable, which indicates if the added attraction is pet friendly, will be set to True
    if new_attraction_pet_friendly == "y":
        new_attraction_pet_friendly = True
    # if the user indicates that the attraction that they would like to add is not pet friendly, the
    # new_attraction_pet_friendly variable, which indicates if the added attraction is pet friendly, will be set to False
    else:
        new_attraction_pet_friendly = False

    #initializes total_count variable which keeps track of the amount of attractions in the database and serves as
    #the variable that defines the attraction number for the added attractions
    total_count = 1
    # gets the collection of Attractions from the database
    docs = db.collection('Attractions').get()
    for doc in docs:
        #total_count increases by 1 after each question in the database is identified
        total_count+=1

    #adds a new document to the attractions database that is titled with the attraction's number and adds all the attributes
    #for that attraction that was set by the user
    db.collection('Attractions').document(str(total_count)).set({"Attraction Name": new_attraction_name, "Type of Attraction": new_attraction_type,
                                                                 "Location": new_attraction_location, "Free Parking": new_attraction_free_parking,
                                                                 "Free WiFi": new_attraction_free_wifi, "Souvenir Shop": new_attraction_souvenir_shop,
                                                                 "Pet Friendly": new_attraction_pet_friendly})
    print("Successfully submitted new attraction!")
    print("Reloading Colorado Attractions list...\n")

    #initializes current_count variable which keeps track of the number of each attraction in the database that is displayed
    current_count = 1
    #loops through each attractions and prints the attraction number and the attraction name
    docs = db.collection('Attractions')
    query = docs.order_by("`Attraction Name`")
    sortedDocs = query.get()
    for doc in sortedDocs:
        print(str(current_count) + ". " + doc.to_dict().get("Attraction Name"))
        #current_count increases by 1 after each attraction and corresponding answer is printed to keep track of the number
        #of each attraction that is displayed from the database
        current_count += 1

    # list of pages that the user can access from the Add a Colorado Attraction page
    print("\n1. Home")
    # prompt that asks the user which page they would like to go to
    full_list_option_choice = input("Select an option above using its corresponding option number\n --> ")

    # if the user selects option 1, they will be taken back to the Home Page, a method
    # called from the home_page.py file
    if full_list_option_choice == "1":
        home_navigation_page()