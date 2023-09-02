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
import json
from dotenv import load_dotenv

load_dotenv(".env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class ActionBooksAPI(Action):
    def name(self) -> Text:
        return "action_get_book_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Current slots:", tracker.current_slot_values())
        print("Latest user message:", tracker.latest_message.get("text"))
        book_name = tracker.get_slot('book_name')
        print(f"Book name: {book_name}")
        base_url = "https://www.googleapis.com/books/v1/volumes"    
        params = {
            "q": f"intitle:{book_name}",
            "country": 'US',
            "key": GOOGLE_API_KEY 
,
        }
    
        response = requests.get(base_url, params=params)
        data = response.json()
        print(json.dumps(data, indent=4))
        

        if "items" in data:
            book_info = data["items"][0]
            self.display_price_info(dispatcher, book_info)
        else:
            dispatcher.utter_message("Book not found.")

        return []
    def display_price_info(self, dispatcher: CollectingDispatcher, book_info):
        sale_info = book_info.get("saleInfo", {})
        print(f" sale_info : {sale_info }")
        saleability = sale_info.get("saleability", {})
        print(f" saleability: {saleability}")
        
    
        if saleability == "FOR_SALE" and "retailPrice" in sale_info:
            retail_price = sale_info["retailPrice"]
            price_amount = retail_price.get("amount", "Price not available")
            currency = retail_price.get("currencyCode", "")
            price_message = f"Price: {price_amount} {currency}"
        else:
            price_message = "Price: Not for sale."
    
        dispatcher.utter_message(price_message)

class ActionBooksAPI(Action):

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
            dispatcher.utter_message("Book not found.")

        return []

    def display_description(self, dispatcher: CollectingDispatcher, book_info):
        volume_info = book_info.get("volumeInfo", {})
        description = volume_info.get("description", "Description not available.")

        dispatcher.utter_message(description)
    
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_find_Books_by_author"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
        # Get user message from Rasa tracker
        author_name = tracker.latest_message.get('author_name')
        print(author_name)

        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': "OPEANAI_API_KEY",
            'Content-Type': 'application/json'
        }
        data = {
            'model': "gpt-3.5-turbo",
            'messages': [
                {'role': 'system', 'content': 'You are  chatbot name "book bot ". You will Find the names of books by author. Maxumum 7 books'},
                {'role': 'user', 'content': 'You: ' + author_name}
            ],
            'max_tokens': 100
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            chatgpt_response = response.json()
            message = chatgpt_response['choices'][0]['message']['content']
            dispatcher.utter_message(message)
            print(message)
        else:
            # Handle error and return an event to indicate the action failed
            dispatcher.utter_message("Sorry, I couldn't generate a response at the moment. Please try again later.")
           