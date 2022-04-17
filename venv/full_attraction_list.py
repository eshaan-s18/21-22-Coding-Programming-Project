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

#method that presents the View Full List of Colorado Attractions page, which provides the user access to a full list of
#all the Colorado Attractions that can be accessed through the program
def view_full_list():
    #imports the home_navigation_page method from the home_page.py file to allow the user access back to the home page
    from home_page import home_navigation_page

    #prints out the View Full List of Colorado Attractions header
    print("\nView Full List of Colorado Attractions:\n")

    #initializes current_count variable which keeps track of the number of each question in the database that is displayed
    current_count = 1

    #gets the collection of Attractions from the database
    docs = db.collection('Attractions').get()
    #loops through each Attraction and prints out the attraction number through current_count and the Attraction Name
    for doc in docs:
        print(str(current_count) + ". " + doc.to_dict().get("Attraction Name"))
        #current_count increases by 1 after each question and corresponding answer is printed to keep track of the number
        #of each question that is displayed from the database
        current_count+=1

    # list of pages and actions that the user can access from the View Full List of Colorado Attractions page
    print("\n1. Home")
    #prompt that asks the user which page they would like to go to
    full_list_option_choice = input("Select an option above using its corresponding option number\n --> ")

    # if the user selects option 3, they will be taken back to the Home Page, a method
    # called from the home_page.py file
    if full_list_option_choice == "1":
        home_navigation_page()

