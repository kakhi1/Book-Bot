# Book-Bot

This is a chatbot project that utilizes the Rasa framework. connect to two different APIs: Google Books API and the OpenAI API. 
The chatbot can provide book information, including description, price, and links to books using the Google Books API. 
Additionally, it can recommend books based on authors and descriptions using the OpenAI API.

## Features

- Retrieve book information from Google Books API.
- Recommend books based on authors and descriptions using the OpenAI API.
- Basic HTML front-end for interacting with the chatbot.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python (3.x recommended) installed on your system.
- Rasa framework installed. You can install it using `pip`:

  ```shell
  pip install rasa

## Installation

Before you can run the chatbot, you need to set up the required environment and install the necessary dependencies.

1. **Python 3**: If you don't have Python 3 installed, you can download and install it from the [official Python website](https://www.python.org/downloads/).

2. **OpenAI API**: You'll need an OpenAI API key. You can obtain one by following the instructions on the [OpenAI website](https://beta.openai.com/signup/).

3. **Google Books API**: You'll also need to set up a Google Books API key. Follow the steps outlined in the [Google Books API documentation](https://developers.google.com/books/docs/v1/getting_started) to obtain your API key.

4. **dotenv**: This project uses `dotenv` to manage environment variables. You can install it using `pip`:

   ```shell
   pip install python-dotenv


### Clone this repository:

- https://github.com/kakhi1/Book-Bot.git
- cd Book-Bot

### Install the required Python dependencies:
- pip install -r requirements.txt

### Set up your API keys:
- Add your Google API key to 'GOOGLE_API_KEY'
- Add your OPENAI API key to 'OPENAI_API_KEY'

  ### Run the Rasa chatbot:
  ```shell
   rasa train
   rasa run

## Usage
- Access the chatbot via the HTML front-end by opening the index.html file in your web browser.
- Interact with the chatbot by providing queries for book information and recommendations.

  ### Running the Rasa Server
  
  To start the Rasa chatbot server, use the following command:
  ```shell
  python -m rasa run --port 8098 --cors "*"

 ### Running the Custom Actions Server
    
    rasa run actions


### Acknowledgments

- Thanks to Rasa for providing the chatbot framework.
- Thanks to Google for the Google Books API.
- Thanks to OpenAI for the recommendation capabilities.
    

## Dockerization

#### To Dockerize the project, we'll create separate Dockerfiles for the Rasa chatbot, custom actions server, and the NGINX frontend server.


## Rasa Chatbot Dockerfile

     ```shell
     docker build . -t <account_username>/<repository_name>:<custom_image_tag>
     docker run -d -p 8098:5005 <account_username>/<repository_name>:<custom_image_tag>

## Custom Actions Server Dockerfile

    ```shell
    docker build . -t <account_username>/<repository_name>:<custom_image_tag>
    docker run -d  <account_username>/<repository_name>:<custom_image_tag>

## NGINX Frontend Dockerfile

    ```shell
    docker build . -t <account_username>/<repository_name>:<custom_image_tag>
    docker run -d -p 80:80 <account_username>/<repository_name>:<custom_image_tag>

 Now you have the Rasa chatbot, custom actions server, and NGINX frontend server running in separate Docker containers.
 When deploying the action server image, you need to add the endpoint.yml file to the Rasa chatbot. Then, the Rasa chatbot URL can be used for front-end post requests.

## Usage

  Access the chatbot via the HTML front-end by opening the index.html file in your web browser.
 Interact with the chatbot by providing queries for book information and recommendations.

### Contact
    
- Kakhi Mtchedluri
- kmchedluri@gmail.com
