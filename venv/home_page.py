#import methods from other files in program
from help_menu import *
from add_attraction import *
from find_colorado_attraction import *
from full_attraction_list import *

#method that presents the Home Page, which serves as the main navigation page for the program
def home_navigation_page():
    # prints out the Home Page header
    print("\nHome Page:\n")

    #list of pages that the user can access from the Home Page
    print("1. Find a Colorado Attraction")
    print("2. View Full List of Colorado Attractions")
    print("3. Add a Colorado Attraction")
    print("4. Help Menu")
    print("5. Quit")

    #prompt that asks the user which page they would like to go to
    home_page_options = input("Select an option above using its corresponding option number\n --> ")

    #if the user selects option 1, they will be taken to the Find a Colorado Attraction page, a method called from the
    #find_colorado_attraction.py file
    if home_page_options == "1":
        find_colorado_attraction()

    #if the user selects option 2, they will be taken to the View Full List of Colorado Attractions page, a method
    #called from the full_attraction_list.py file
    elif home_page_options == "2":
        view_full_list()

    #if the user selects option 3, they will be taken to the Add a Colorado Attraction page, a method
    #called from the add_attraction.py file
    elif home_page_options == "3":
        add_colorado_attraction()

    #if the user selects option 4, they will be taken to the Help Menu page, a method
    #called from the help_menu.py file
    elif home_page_options == "4":
        help_menu()

    #if the user selects option 5, they program will print out a thank you message and the program will stop
    else:
        print("Thank you for using the Official Colorado Tourism Bureau Attraction Suggester, we hope you found the perfect Colorado Attraction for you!")

