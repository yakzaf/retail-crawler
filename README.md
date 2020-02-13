# Retail Crawler
A simple Django-based web application that scrapes discounted items from retail store websites and displays them in cards. 

## Installation

1. Install and configure virtualenv.
    * To enter the environment, run:
    ```source your-env-folder/bin/activate```

    * To exit it, run: 
    ```deactivate```
2. Clone the repo
3. Install the project dependancies
```
pip3 install -r requirements.txt
```
4. Create a .env file and fill it up with the environment-specific information (e.g. database information, SECRET_KEY)

## Acessing the API

The project includes a simple API (made with Django Rest Framework) that returns basic info about the products: title, link to the item, regular price, and sale price.
```
/api/v1/hm/items/
```
The amount of items needed can be specified with the ```amount``` query string.
