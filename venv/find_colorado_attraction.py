#packages imported
import numpy as np
import pandas as pd
import googlemaps
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim

#pull database from Cloud Firestore
db = firestore.client()

#method that allows the user to select their location preferences from four provided options
def select_location_preference():
    #prompt that asks the user to select a preferred location in Colorado for their ideal attraction from four provided options
    location_preference = input("Please select a preferred location in Colorado for your attraction from the options provided: \n1. Denver \n2. Colorado Springs "
                                "\n3. Glenwood Springs \n4. Colorado Mountain Cities\n--> ")
    #if the user selects option 1, the method will return their preferred location for an attraction: Denver
    if location_preference == '1':
        return "Denver"
    # if the user selects option 2, the method will return their preferred location for an attraction: Colorado Springs
    elif location_preference == '2':
        return "Colorado Springs"
    # if the user selects option 3, the method will return their preferred location for an attraction: Glenwood Springs
    elif location_preference == '3':
        return "Glenwood Springs"
    # if the user selects option 4, the method will return their preferred location for an attraction: Colorado Mountain Cities
    elif location_preference == '4':
        return "Colorado Mountain Cities"

    #if the user does not select any valid options, they will receive an error message and will have to redo the
    #location preference selection process as the method is recursively called
    else:
        print("~Error: Not a valid option, please try again~\n")
        select_location_preference()

#method that allows the user to select their attraction type preferences from 5 initial options provided
def select_attraction_type_preference():
    #prompt that asks the user to select a preferred type of attraction for their ideal attraction from five provided options
    attraction_type_preference = input("\nPlease select a preferred type of attraction from the corresponding option numbers provided: \n1. Landmark \n2. Activity "
                                   "\n3. Exhibit \n4. Mountains \n5. Choose Multiple Options \n--> ")

    #if the user selects option 1, the method will return their preferred type of attraction: Landmark
    if attraction_type_preference == '1':
        return "Landmark"
    #if the user selects option 2, the method will return their preferred type of attraction: Activity
    elif attraction_type_preference == '2':
        return "Activity"
    #if the user selects option 3, the method will return their preferred type of attraction: Exhibit
    elif attraction_type_preference == '3':
        return "Exhibit"
    #if the user selects option 4, the method will return their preferred type of attraction: Mountains
    elif attraction_type_preference == '4':
        return "Mountains"
    #if the user selects option 5, they will be able to select multiple attraction types for their ideal attraction,
    #the user is able to select 2-3 attraction types for an attraction
    elif attraction_type_preference == '5':
        #initializes the variables option_1_choice and option_2_choice, which will both hold the user's selections for
        #their first and second attraction type choices
        option_1_choice = ""
        option_2_choice = ""

        #prompt that asks the user to select their first attraction type for their ideal attraction
        multiple_option_1 = input("Please select your first preferred type of attraction from the corresponding option numbers provided above. \n --> ")
        #if the user selects option 1, option_1_choice, which holds the user's selection for their first attraction type choice,
        #is set to equal "Landmark"
        if multiple_option_1 == '1':
            option_1_choice = "Landmark"
        # if the user selects option 2, option_1_choice is set to equal "Activity"
        elif multiple_option_1 == '2':
            option_1_choice = "Activity"
        # if the user selects option 3, option_1_choice is set to equal "Exhibit"
        elif multiple_option_1 == '3':
            option_1_choice = "Exhibit"
        # if the user selects option 4, option_1_choice is set to equal "Mountains"
        elif multiple_option_1 == '4':
            option_1_choice = "Mountains"

        #prompt that asks the user to select their second attraction type for their ideal attraction
        multiple_option_2 = input("Please select your second preferred type of attraction from the corresponding option numbers provided above. \n --> ")
        #if the user selects option 1, option_2_choice, which holds the user's selection for their second attraction type choice,
        #is set to equal "Landmark"
        if multiple_option_2 == '1':
            option_2_choice = "Landmark"
        #if the user selects option 2, option_2_choice is set to equal "Activity"
        elif multiple_option_2 == '2':
            option_2_choice = "Activity"
        #if the user selects option 3, option_2_choice is set to equal "Exhibit"
        elif multiple_option_2 == '3':
            option_2_choice = "Exhibit"
        #if the user selects option 4, option_2_choice is set to equal "Mountains"
        elif multiple_option_2 == '4':
            option_2_choice = "Mountains"

        #prompt that asks the user to if they would like to select a third preferred attraction type
        third_option_choice = input("Would you like a third preferred type option? (y/n) \n --> ")
        #if the user selects yes to this prompt they are able to select a third preferred attraction type
        if third_option_choice == "y":
            #prompt that asks the user to select a third preferred attraction type
            multiple_option_3 = input("Please select your third preferred type of attraction from the options provided above. \n --> ")
            # initializes the variable option_3_choice, which will hold the user's selections for their third attraction type choice
            option_3_choice = ""
            #if the user selects option 1, option_3_choice is set to equal "Landmark"
            if multiple_option_3 == '1':
                option_3_choice = "Landmark"
            # if the user selects option 2, option_3_choice is set to equal "Activity"
            elif multiple_option_3 == '2':
                option_3_choice = "Activity"
            # if the user selects option 3, option_3_choice is set to equal "Exhibit"
            elif multiple_option_3 == '3':
                option_3_choice = "Exhibit"
            # if the user selects option 4, option_3_choice is set to equal "Mountains"
            elif multiple_option_3 == '4':
                option_3_choice = "Mountains"

            #once the first, second, and third preferred attraction types are chosen, the method returns all three options
            #in a format that matches how they are displayed in the database for easier query matching
            return option_1_choice + ", " + option_2_choice + ", " + option_3_choice
        else:
            #if the user does not want a third preferred attraction type choice, the method will return the two options
            #selected by the user in a format that matches how they are displayed in the database for easier query matching
            return option_1_choice + ", " + option_2_choice

    #if the user selects a number corresponding to an invalid option, they will be given a warning message and will have
    #to restart their attraction type preference selection process
    else:
        return "~Error: Not a valid option, please try again~\n"

    select_attraction_type_preference()



#method that converts from miles to meters which will be used as a radius from the selected attracted to find restaurants nearby
def miles_to_meters(miles):
    try:
        return miles * 1609.34
    except:
        return 0

#method that takes in the selected attraction and provides information on it like its address and the top 3 rated restaurants
#that are in a 10 mile radius of the attractions
def filtered_attraction_information(selected_attraction, filtered_attraction_list):
    #imports the home_navigation_page method from the home_page.py file to allow the user access back to the home page
    from home_page import home_navigation_page

    #accesses the user-selected attraction and prints the name of the attraction
    print("\n"+ filtered_attraction_list[selected_attraction - 1] + " Information:")

    #initializes geolocator variable from Google Maps API
    geolocator = GoogleV3(api_key="")
    #initializes the address variable which is geocoded using the name of the attraction
    address = geolocator.geocode(filtered_attraction_list[selected_attraction - 1])

    #prints the address of the location
    print("Address: " + str(address))

    #connects to Google Places API using API Key
    map_client = googlemaps.Client('')

    #initializes the location variable which is equal to the longitude and latitude of the attraction
    location = (address.latitude, address.longitude)

    #initializes the search string variable which Google Places API uses as a keyword to search surrounding places using
    search_string = "unique restaurants"
    #initializes the distance variable as 10 miles, which is converted to meters for the purpose of the API
    distance = miles_to_meters(10)

    #initializes necessary variables for the implementation of the nearby search process
    list = []
    payload={}
    headers = {}

    #sets the parameters for the nearby place search including the location of the attraction, the keyword to search
    #surrounding places using, the name to reference nearby places, and the radius from the attraction to search for
    #nearby places in
    response = map_client.places_nearby(
        location = location,
        keyword = search_string,
        name = 'unique restaurants',
        radius = distance

    )

    #loop that adds the results for the nearby search to an array called ratings where the results can be accessed
    i = 0
    ratings = []
    while(i < len(response['results'])):
        ratings.append(str(response['results'][i]['rating']) + " stars - " + response['results'][i]['name'])
        i+=1
        #the ratings array is sorted from highest rating to lowest rating
    ratings.sort(reverse=True)

    near_restaurant_count = 0
    print("\nTop-Rated Nearby Restaurants: ")

    #loop that prints the top 3 highest rated restaurants that are nearby the attraction
    while(near_restaurant_count < 3):
        print(ratings[near_restaurant_count])
        near_restaurant_count+=1

    #prompt that asks the user if they would like to repeat the process of viewing the information of another attraction,
    #go back to the home navigation page, or restart the process of viewing the information for the attraction they have currently selected
    repeat_selected_attraction_info = input(
        "\nIf you would like to get information on another attractions, please type its corresponding number"
        " (type 'home' to go to the home page or type 'restart' to set new preferences)\n --> ")
    #if the user responds to the prompt with 'home', they will be taken back to the Home Page, a method
    # called from the home_page.py file
    if repeat_selected_attraction_info == "home":
        home_navigation_page()
    #if the user responds to the prompt with 'restart', the method will restart for the same attraction info
    elif repeat_selected_attraction_info == 'restart':
        find_colorado_attraction()
    #if the user responds with the corresponding number of another attraction, the method will restart, but it will now
    #display the information for a different attraction
    else:
        filtered_attraction_information(int(repeat_selected_attraction_info), filtered_attraction_list)

#method that allows the user to find the ideal Colorado Attraction for them by allowing the user to select desired attributes
#that they expect to be in their ideal Colorado Attraction, and a query from the database is filtered and displays the attractions
#that match the users selected preferences
def find_colorado_attraction():
    #imports the home_navigation_page method from the home_page.py file to allow the user access back to the home page
    from home_page import home_navigation_page

    #prints out the Find a Colorado Attraction header
    print("\nFind a Colorado Attraction:\n")


    #initialized variable that represent operator values that are necessary for the query to know whether to look for a match case
    #or to not look for any match case
    location_operator = ""
    attraction_type_operator = ""
    free_parking_operator = ""
    free_wifi_operator = ""
    souvenir_shop_operator = ""
    pet_friendly_operator = ""

    #prompt that asks the user if they have any location preference for their ideal attraction
    location_preference = input("Do you have a preference for the location of your Colorado Attractions? (y/n)\n --> ")
    #if the user selects yes, they will be taken to the method which will allow them to set their Colorado location preferences
    if location_preference == "y":
        #the user selected location preference is saved in the location_preference variable, and the location_operator is
        #set to ==, which indicates to the search query that it is looking for a match case
        location_preference = select_location_preference()
        location_operator = "=="
    else:
        #if the user selects no, the location_preference variable will be set to none, and the location_operator is set to !=,
        #which indicates to the search query that it is not looking for a match case
        location_preference = "NO LOCATION PREFERENCE"
        location_operator = "!="

    #prompt that asks the user if they have any preference of the type of attraction for their ideal attraction
    attraction_type_preference = input("Do you have a preference for the type of attraction your Colorado Attractions are? (y/n)\n --> ")
    #if the user selects yes, they will be taken to the method which will allow them to set their preferences for the type of attraction
    if attraction_type_preference == "y":
        # the user selected attraction type preference is saved in the attraction_type_preference variable, and the attraction_type_operator
        #is set to ==, which indicates to the search query that it is looking for a match case
        attraction_type_preference = select_attraction_type_preference()
        attraction_type_operator = "=="
    else:
        #the user selects no, the attraction_type_preference variable will be set to none, and the attraction_type_operator
        #is set to !=, which indicates to the search query that it is not looking for a match case
        attraction_type_preference = "NO ATTRACTION TYPE PREFERENCE"
        attraction_type_operator = "!="

    #prompt that asks the user if they want to set a filter for their attractions to be displayed only if they have free parking
    free_parking_preference = input("Do you want to filter your Colorado Attractions to locations that have free parking? (y/n)\n --> ")
    #if the user selects yes, the free parking preference (True) is saved in the free_parking_preference variable, and the
    #free_parking_operator is set to ==, which indicates to the search query that it is looking for a match case
    if free_parking_preference == "y":
        free_parking_preference = True
        free_parking_operator = "=="

    #if the user selects no,the free_parking_preference variable will be set to none, and the free_parking_operator is
    #set to !=, which indicates to the search query that it is not looking for a match case
    else:
        free_parking_preference = "NO FREE PARKING PREFERENCE"
        free_parking_operator = "!="

    #prompt that asks the user if they want to set a filter for their attractions to be displayed only if they have free wifi
    free_wifi_preference = input("Do you want to filter your Colorado Attractions to locations that have free WiFi? (y/n)\n --> ")
    #if the user selects yes, the free wifi preference (True) is saved in the free_wifi_preference variable, and the
    #free_wifi_operator is set to ==, which indicates to the search query that it is looking for a match case
    if free_wifi_preference == "y":
        free_wifi_preference = True
        free_wifi_operator = "=="
    #if the user selects no, the free_wifi_preference variable will be set to none, and the free_wifi_operator is
    #set to !=, which indicates to the search query that it is not looking for a match case
    else:
        free_wifi_preference = "NO FREE WIFI PREFERENCE"
        free_wifi_operator = "!="

    #prompt that asks the user if they want to set a filter for their attractions to be displayed only if they have a souvenir shop
    souvenir_shop_preference = input("Do you want to filter your Colorado Attractions to locations that have a souvenir shop? (y/n)\n --> ")
    #if the user selects yes, the souvenir shop preference (True) is saved in the souvenir_shop_preference variable, and the
    #souvenir_shop_operator is set to ==, which indicates to the search query that it is looking for a match case
    if souvenir_shop_preference == "y":
        souvenir_shop_preference = True
        souvenir_shop_operator = "=="
    #if the user selects no, the souvenir_shop_preference variable will be set to none, and the souvenir_shop_operator is
    #set to !=, which indicates to the search query that it is not looking for a match case
    else:
        souvenir_shop_preference = "NO SOUVENIR SHOP PREFERENCE"
        souvenir_shop_operator = "!="

    #prompt that asks the user if they want to set a filter for their attractions to be displayed only if they are pet friendly
    pet_friendly_preference = input("Do you want to filter your Colorado Attractions to locations that are pet friendly? (y/n)\n --> ")
    #if the user selects yes, the pet friendly preference (True) is saved in the pet_friendly_preference variable, and the
    #pet_friendly_operator is set to ==, which indicates to the search query that it is looking for a match case
    if pet_friendly_preference == "y":
        pet_friendly_preference = True
        pet_friendly_operator = "=="
    else:
        # if the user selects no,the pet_friendly_preference variable will be set to none, and the pet_friendly_operator is
        # set to !=, which indicates to the search query that it is not looking for a match case
        pet_friendly_preference = "NO PET FRIENDLY PREFERENCE"
        pet_friendly_operator = "!="

    #count that keeps track of the number of attractions that fit the users desired attributes that are printed
    current_count = 1
    #array that holds the names of the attractions that fit the users desired attributes
    filtered_attractions_list = []

    #initialized docs variables which holds references to all the attractions that the query matches with the users desired attributes
    docs = db.collection('Attractions').where("Location", location_operator, location_preference).where("`Type of Attraction`", attraction_type_operator, attraction_type_preference)\
            .where("`Free Parking`", free_parking_operator, free_parking_preference).where("`Free WiFi`", free_wifi_operator, free_wifi_preference)\
            .where("`Souvenir Shop`", souvenir_shop_operator, souvenir_shop_preference).where("`Pet Friendly`", pet_friendly_operator, pet_friendly_preference).get()
    print('~~~~~~~~~~~~~~~~~~~~~~~~\n')
    #loop that displays the attraction number and name of the attractions that fit the users desired attributes and adds
    #them to the filtered_attractions_list array
    for doc in docs:
        print(str(current_count) + ". " + doc.to_dict().get("Attraction Name"))
        current_count += 1
        filtered_attractions_list.append(doc.to_dict().get("Attraction Name"))

    #prompt that asks the user if they would like to view information of one of the attractions that matches their desired attributes,
    #go back to the home navigation page, or restart the process of setting their desired attributes and finding attractions that fit them
    selected_attraction_info = input("\nType the corresponding number to the attraction you would like to get information "
                                     "about (type 'home' to go to the home page or type 'restart' to set new preferences)\n --> ")

    # if the user selects option 1, they will be taken back to the Home Page, a method
    # called from the home_page.py file
    if selected_attraction_info == "home":
        home_navigation_page()
    # if the user responds to the prompt with 'restart', the method will restart and the user can select new desired attributes
    elif selected_attraction_info == 'restart':
        find_colorado_attraction()
    else:
    #if the user responds with the number corresponding to the attraction that matches their desired attributes, they
    #will be taken to a method that displays the information for this specific attraction
        filtered_attraction_information(int(selected_attraction_info), filtered_attractions_list)