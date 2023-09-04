# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from tkinter import EventType
from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
import os
import json
from dotenv import load_dotenv
import  openai

load_dotenv(".env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class ActionBooksPrice(Action):
    def name(self) -> Text:
        return "action_get_book_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        book_name = tracker.get_slot('book_name')
        print(f"Book name: {book_name}")
        base_url = "https://www.googleapis.com/books/v1/volumes"    
        params = {
            "q": f"intitle:{book_name}",
            "country": 'US',
            "key": GOOGLE_API_KEY,
        }
    
        response = requests.get(base_url, params=params)
        data = response.json() 

        if "items" in data:
            book_info = data["items"][0]
            self.display_price_info(dispatcher, book_info)
        else:
            dispatcher.utter_message("I'm sorry, but it seems like we don't have the book you're looking for.")

        return []
    def display_price_info(self, dispatcher: CollectingDispatcher, book_info):
        sale_info = book_info.get("saleInfo", {})       
        saleability = sale_info.get("saleability", {})       
    
        if saleability == "FOR_SALE" and "retailPrice" in sale_info:
            retail_price = sale_info["retailPrice"]
            price_amount = retail_price.get("amount", "Price not available")
            currency = retail_price.get("currencyCode", "")
            price_message = f"Price: {price_amount} {currency}"
        else:
            price_message = "Not currently available for sale."
    
        dispatcher.utter_message(price_message)

class ActionBooksDescription(Action):

    def name(self) -> Text:
        return "action_get_book_info"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        book_name = tracker.get_slot('book_name')
        base_url = "https://www.googleapis.com/books/v1/volumes"
    
        params = {
            "q": f"intitle:{book_name}",
            "country": 'US',
            "key": GOOGLE_API_KEY ,
            
        }
    
        response = requests.get(base_url, params=params)
        data = response.json()
        if "items" in data:
            book_info = data["items"][0]
            self.display_description(dispatcher, book_info)
        else:
            dispatcher.utter_message("I'm sorry, but it seems like we don't have the book you're looking for.")

        return []

    def display_description(self, dispatcher: CollectingDispatcher, book_info):
        volume_info = book_info.get("volumeInfo", {})
        description = volume_info.get("description", "Description not available.")

        dispatcher.utter_message(description)
    
        return []

class ActionGetBooksNamesByAuthor(Action):
    def name(self):
        return "action_find_Books_by_author"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        # OpenAI API 
        openai.api_key = OPENAI_API_KEY

        # Get the value of the 'author_name' slot
        author_name = tracker.get_slot("author_name")

        # Define the messages for the OpenAI GPT-3 request
        messages = [
            {"role": "system", "content":"Name up to seven of the best  books by this author, but please only include the book titles."},
            {"role": "user", "content": f"Generate content by {author_name}"}
        ]

        # Create a request to the OpenAI GPT-3 model
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Get the response from the model
        response = completion.choices[0].message["content"]

        # Send the response back to the user
        dispatcher.utter_message(response)

class ActionBooksLink(Action):

    def name(self) -> Text:
        return "action_get_book_link"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Current slots:", tracker.current_slot_values())
        print("Latest user message:", tracker.latest_message.get("text"))
        book_name = tracker.get_slot('book_name')
        print(f"wignis saxeli:{book_name}")
        base_url = "https://www.googleapis.com/books/v1/volumes"  
        params = {
            "q": f"intitle:{book_name}",
            "country": 'US',
            "key": GOOGLE_API_KEY ,          
        }
    
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)

        if "items" in data:
            book_info = data["items"][0]
            self.display_description(dispatcher, book_info)
        else:
            dispatcher.utter_message("I'm sorry, but it seems like we don't have the book you're looking for.")

        return []

    def display_description(self, dispatcher: CollectingDispatcher, book_info):
        volume_info = book_info.get("volumeInfo", {})
        link = volume_info.get("previewLink", "Apologies, but it seems that the link for purchase is currently unavailable.")

        dispatcher.utter_message(link)
    
        return []

class ActionGetBookBy(Action):
    def name(self):
        return "action_get_book_recommendation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        # OpenAI API 
        openai.api_key = "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"
        # Get the value of the 'author_name' slot
        recommendation = tracker.get_slot("recommendation")
        print(f"recomendatia:{recommendation}")

        # Define the messages for the OpenAI GPT-3 request
        messages = [
            {"role": "system", "content":"You should recommend {recommendation} one book. write only book name, no description, no author, just book name."},
            {"role": "user", "content": f"Generate content by {recommendation}"}
        ]

        # Create a request to the OpenAI GPT-3 model
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Get the response from the model
        response = completion.choices[0].message["content"]

        # Send the response back to the user
        dispatcher.utter_message(response)
        return [SlotSet("book_name", response)]
    
class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Reset all slots in the tracker
        for slot in tracker.slots.keys():
            tracker.slots[slot] = None
            print(f"darestartda ")
        
        # Clear any active forms
        tracker.active_form = {}
        
        # Respond to the user
        dispatcher.utter_message(template="utter_restart")
        
        # Return an empty list as the action result
        return []
    
    
    

    
    