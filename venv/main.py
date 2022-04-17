#packages imported
import numpy as np
import pandas as pd
import googlemaps
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from pathlib import Path
import pandas as pd

#connecting program with firebase
cred = credentials.Certificate("venv/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from home_page import *
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim

#import methods from other files in program
from add_attraction import *
from find_colorado_attraction import *
from full_attraction_list import *
from help_menu import *

#pull database from Cloud Firestore
db = firestore.client()


#introductory page
print('\n')
print("                         Welcome to the Official Colorado Tourism Bureau Attraction Suggester")
print("-----Using this program you will be able to explore the major attractions in Colorado based on your desired attributes-----\n")

#calls method that presents the Home Page, which serves as the main navigation page for the program
home_navigation_page()