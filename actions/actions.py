# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
from dotenv import load_dotenv
load_dotenv (".env")
GOOGLE_API_KEY = os.getenv ('GOOGLE_API_KEY')

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
        api_key = GOOGLE_API_KEY
        base_url = "https://www.googleapis.com/books/v1/volumes"
    
        params = {
            "q": f"intitle:{book_name}",
            "key": api_key,
        }
    
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)