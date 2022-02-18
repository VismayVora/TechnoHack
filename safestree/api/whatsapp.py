import requests
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


def send_message(request, user, message):
    url = "https://api.wassenger.com/v1/messages"

    payload = {
        "phone": str(user.number),
        "message": message
    }
    headers = {
        "Content-Type": "application/json",
        "Token": "54440d1512c24f16a31798a727a9d856813c3a024b2d0efb3d7fa4a7bf137ec434fa620e7374f485"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text) 