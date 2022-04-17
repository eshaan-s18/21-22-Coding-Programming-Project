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

#method that presents the Help Menu, which provides the user access to the How to Use Colorado Attraction Suggester page
#and the interactive Q&A page
def help_menu():
    #imports the home_navigation_page method from the home_page.py file to allow the user access back to the home page
    from home_page import home_navigation_page

    #prints out the Help Menu page header
    print("\nHelp Menu:\n")

    #list of pages that the user can access from the Help Menu
    print("1. How to Use Colorado Attraction Suggester")
    print("2. Q&A")
    print("3. Home")

    #prompt that asks the user which page they would like to go to
    help_menu_option_choice = input("Select an option above using its corresponding option number\n --> ")

    #if the user selects option 1, they will be taken to the How to Use Colorado Attraction Suggester page
    if help_menu_option_choice == "1":
        how_to_use()

    #if the user selects option 1, they will be taken to the Q&A page
    elif help_menu_option_choice == "2":
        interactive_Q_and_A()

    #if the user selects option 3, they will be taken back to the Home Page, a method
    #called from the home_page.py file
    else:
        home_navigation_page()

#method that presents the How to Use Colorado Attraction Suggester page, which provides the user information on how to
#use Colorado Attraction Suggester
def how_to_use():
    # imports the home_navigation_page method from the home_page.py file to allow the user access back to the home page
    from home_page import home_navigation_page

    #prints out the How to Use Colorado Attraction Suggester page header
    print("How to Use Colorado Attraction Suggester:\n")

    #prints out the 4 main pages Colorado Attraction Suggester Consists of
    print("The Colorado Attraction Suggester consists of 4 main pages: Find a Colorado Attraction, View Full List of Colorado Attractions, Add a Colorado Attraction, and Help Menu\n")

    #prints out information on how to use the Find a Colorado Attraction page
    print("Find a Colorado Attraction:")
    print("The Find a Colorado Attraction Page is the main page you will use. This page allows you to find the perfect Colorado Attraction to fit your needs."
          " By simply answering a couple questions about location, attraction, and amenity preferences, the program will filter attractions from the Colorado Attractions "
          "database and output the attractions that are best for you based on your preferences.\n")

    # prints out information on how to use the View Full List of Colorado Attractions page
    print("View Full List of Colorado Attractions:")
    print("Before you find the best Colorado Attraction for your preferences, you can view our entire database of Colorado Attractions by selecting this menu. The list of "
          "Colorado Attractions will pop up for you to look through, and it will help you gain a sense of the type of attractions Colorado has to offer.\n")

    # prints out information on how to use the Add a Colorado Attraction page
    print("Add a Colorado Attraction:")
    print("Do you know an amazing Colorado Attraction that isn't on the list? Using this page you can add that Colorado Attraction to the database to be filtered and accessed "
          "while you and others find a the best Colorado Attraction!\n")

    # prints out information on how to use the Help Menu page
    print("Help Menu:")
    print("The Help Menu provides you access to information on how to use Colorado Attraction Suggester and an "
          "interactive Q&A page where you can ask questions and answer unanswered questions.\n")


    #list of pages that the user can access from the How to Use Colorado Suggester page
    print("1. Back")
    print("2. Home")

    #prompt that asks the user which page they would like to go to
    how_to_use_options = input("Select an option above using its corresponding option number\n --> ")

    #if the user selects option 1, they will be taken back to the Help Menu page
    if how_to_use_options == "1":
        help_menu()

    # if the user selects option 2, they will be taken back to the Home Page, a method
    # called from the home_page.py file
    else:
        home_navigation_page()



def ask_question(total, question):
    # adds document titled with the question number for the new question to the database, adds the question asked by
    # the user, and initially sets the answer to "0 answers"
    if question == "cancelled selection":
        print("Returning back to Q&A page")
        interactive_Q_and_A()
    else:
        db.collection('Questions').document(str(total)).set({"Question": question, "Answer": "0 answers"})

        print("Successfully submitted question! ")
        print("Reloading questions and answers...\n")
        # reloads the questions and answers by calling the method interactive_Q_and_A()
        interactive_Q_and_A()

def answer_question(answer_number, answer):
    if answer_number == "cancelled selection":
        print("Returning back to Q&A page")
        interactive_Q_and_A()
    else:
        # adds the answers to the document containing the question that the user's answer corresponds to
        db.collection('Questions').document(answer_number).set({"Answer": answer}, merge=True)

        print("Successfully answered question " + answer_number + "!")
        print("Reloading questions and answers...\n")
        # reloads the questions and answers by calling the method interactive_Q_and_A()
        interactive_Q_and_A()

def interactive_Q_and_A():
    # imports the home_navigation_page method from the home_page.py file to allow the user access back to the home page
    from home_page import home_navigation_page

    #prints out the Q&A page header
    print("Q&A:\n")

    #initializes total_count variable which keeps track of the amount of questions in the database that are presented
    #to the user and serves as the variable that defines the question number for the added questions
    total_count = 1

    #gets the collection of Questions from the database
    docs = db.collection('Questions').get()
    #loops through each question and prints the question number, the question, and the answer corresponding to it
    for doc in docs:
        print("Question " + str(total_count) + ": " + str(doc.to_dict().get("Question")))
        print("~Answer: " + doc.to_dict().get("Answer") + '\n')
        #total_count increases by 1 after each question and corresponding answer is printed to keep track of the number
        #of questions in the database
        total_count = total_count + 1

    #list of pages and actions that the user can access from the Q&A Page
    print("\n1. Ask a Question")
    print("2. Answer a Question")
    print("3. Back")
    print("4. Home")

    #prompt that asks the user which option they would like to select
    questions_answers_options = input("Select an option above using its corresponding option number\n --> ")

    # if the user selects option 1, they will be able to ask a question that will be added to the list of questions for
    #the Q&A section
    if questions_answers_options == "1":
        # prompt that asks the user to input their question
        question_asked = input("What is your question? (Type 'cancel' to cancel your selection)\n --> ")
        if question_asked == "cancel":
            ask_question("cancelled selection")
        else:
            ask_question(total_count, question_asked)

    #if the user selects option 2, they will be able to answer xan existing question, and that answer will be added to
    #the database for its corresponding questions
    elif questions_answers_options == "2":
        #prompt that asks the user to input the question number of the question they would like to answer
        question_answered_number = input("Type the corresponding question number to the question you would like to answer (Type 'cancel' to cancel your selection)\n --> ")
        #prompt that asks the user to input their answers to the question they have selected
        if question_answered_number != "cancel":
            question_answer = input("Type in your answer to question " + question_answered_number + "\n --> ")
        if question_answered_number == "cancel":
            answer_question("cancelled selection", "cancelled selection")
        else:
            answer_question(question_answered_number, question_answer)

    #if the user selects option 3, they will be taken back to the Help Menu
    elif questions_answers_options == "3":
        help_menu()

    # if the user selects option 3, they will be taken back to the Home Page, a method
    #git called from the home_page.py file
    elif questions_answers_options == "4":
        home_navigation_page()