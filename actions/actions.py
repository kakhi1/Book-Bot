# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
from dotenv import load_dotenv
load_dotenv (".env")
GOOGLE_API_KEY = os.getenv ('GOOGLE_API_KEY')



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
# class ActionBooksAPI(Action):

#     def name(self) -> Text:
#         return "get_book-prize"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         book_name = tracker.get_slot('book_name') 
#         print(f"Identified price is {book_name }")
#         api_key = "AIzaSyAKUxMdiJmC5sQZ7xpnkoi-Qpt1J4Afcog"
#         base_url = "https://www.googleapis.com/books/v1/volumes"
    
#         params = {
#             "q": f"intitle:{book_name}",
#             "key": api_key,
#         }
    
#         response = requests.get(base_url, params=params)
#         data = response.json()
    
#         if "items" in data:
#             book_info = data["items"][0]
#             return book_info
#         else:
#             return None
#         dispatcher.utter_message(text="Hello World!")

#         return []        

class ActionGetBookPrice(Action):

    def name(self) -> Text:
        return "action_get_book_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        book_name = tracker.get_slot('book_name')
        print(f"Identified book name is {book_name}")
        
        api_key = GOOGLE_API_KEY
        base_url = "https://www.googleapis.com/books/v1/volumes"
    
        params = {
            "q": f"intitle:{book_name}",
            "key": api_key,
        }
    
        response = requests.get(base_url, params=params)
        data = response.json()
    
        if "items" in data:
            book_info = data["items"][0]
            sale_info = book_info.get("saleInfo", {})
            saleability = sale_info.get("saleability", "NOT_FOR_SALE")

            if saleability == "FOR_SALE":
                price_info = sale_info.get("retailPrice", {})
                price_amount = price_info.get("amount", "Price not available")
                currency = price_info.get("currencyCode", "")

                if price_amount != "Price not available":
                    price_response = f"Price: {price_amount} {currency}"
                else:
                    price_response = "Price: Price not available."
            else:
                price_response = "Price: Not for sale."
            
            dispatcher.utter_message(text=price_response)
            
        else:
            dispatcher.utter_message(text="Book not found.")
        
        return []