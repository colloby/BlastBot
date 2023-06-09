#! python3
import requests
import time
from bs4 import BeautifulSoup
import json
import datetime

# URL of the webpage to scrape
url = "https://blastpremier.com/tickets/"

# Discord webhook URL to post notifications
discord_webhook_url = "you discord webhook"

while True:
    # Send a GET request to the webpage and store the response
    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the ticket availability message in the HTML
    availability_msg_elem = soup.find("p", {"class": "mb-3 mt-3"})

    #Get the current hour and min of the day
    hour = datetime.datetime.now().hour
    min = datetime.datetime.now().minute

    if availability_msg_elem is not None:
        availability_msg = availability_msg_elem.text.strip()

        # Check if the message indicates that tickets are available
        if "Check back later for ticket availability" in availability_msg:
            #if tickets are not yet available, only post an update it if is between 10:00-10:10 CST, or 16:00-16:10 CST
            if (hour == 10 or hour == 16) and min <= 10:
                message = {"content": "Tickets for Blast Premier Spring Final 2023 are still not available"}
                
                # Send a POST request to the Discord webhook URL with the notification message
                response = requests.post(discord_webhook_url, json=message)
                response.raise_for_status()  # Raise an exception if the request was not successful
        elif "Tickets are now available" in availability_msg:
            # Create a JSON payload with the notification message
            message = {"content": "@everyone Tickets for Blast Premier Spring Final 2023 might be available? I'm dumb so I'm not sure"}
            
            # Send a POST request to the Discord webhook URL with the notification message
            response = requests.post(discord_webhook_url, json=message)
            response.raise_for_status()  # Raise an exception if the request was not successful
            break
        else:
            # Create a JSON payload with the notification message
            message = {"content": "@everyone Tickets for Blast Premier Spring Final 2023 are now available!"}
            
            # Send a POST request to the Discord webhook URL with the notification message
            response = requests.post(discord_webhook_url, json=message)
            response.raise_for_status()  # Raise an exception if the request was not successful
            break
    else:
        message = {"content": "@everyone Error - could not determine whether tickets were available"}
        
        # Send a POST request to the Discord webhook URL with the notification message
        response = requests.post(discord_webhook_url, json=message)
        response.raise_for_status()  # Raise an exception if the request was not successful
        break
    
    # Wait for 10 minutes before checking again
    time.sleep(600)
