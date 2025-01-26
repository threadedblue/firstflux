#!/usr/bin/env python

from urllib.parse import urlparse
from pathlib import Path
import sys
import os
import requests
import time
from PIL import Image
from io import BytesIO
import logging
import json
import base64
import argparse

IMAGE_PROMPT  = "image_prompt"
LOG_FILE = "first.logger"

def imageEncode(prompt): 
    if IMAGE_PROMPT in  prompt:
        with open(prompt[IMAGE_PROMPT], "rb") as image_file:
            prompt[IMAGE_PROMPT] = base64.b64encode(image_file.read()).decode('utf-8')
    return prompt

parser = argparse.ArgumentParser(description="Handle POSIX-style prompts in Python")
parser.add_argument("-p", "--prompt", help="Prompt file.")

# Parse arguments
args = parser.parse_args()

# Create a custom logger
log = logging.getLogger(LOG_FILE)

# Set the logging level
log.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LOG_FILE)

# Set levels for handlers
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

log.addHandler(console_handler)
log.addHandler(file_handler)
# Local file URL
file_url = args.prompt

# Read the file content
log.info("Reading prompt file=" + file_url)
with open(file_url, 'r', encoding='utf-8') as file:
    prompt = json.load(file)
log.debug("prompt=" + str(prompt))

image_path = "scene-office1.png"

log.info("Create base64_image")
imageEncode(prompt)
log.debug("prompt=" + str(prompt))

log.info("Post call")

request = requests.post(
    'https://api.bfl.ml/v1/flux-pro-1.1',
    headers = {
        'accept': 'application/json',
        'x-key': os.environ.get("BFL_API_KEY"),
        'Content-Type': 'application/json',
    },
    json = prompt
).json()

log.debug(request)

request_id = request["id"]

log.info("Response loop")
while True:
    time.sleep(0.5)
    result = requests.get(
        'https://api.bfl.ml/v1/get_result',
        headers={
            'accept': 'application/json',
            'x-key': os.environ.get("BFL_API_KEY"),
        },
        params={
            'id': request_id,
        },
    ).json()

    if result["status"] == "Ready":
        log.debug("1")
        log.info(f"Result: {result['result']['sample']}")
        break
    else:
        log.info(f"Status: {result['status']}")



# The image URL from the response
image_url = result['result']['sample']

# Fetchthe image from the URL
log.info("Getting the image")
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Load the image into Pillow
    log.info("Showing the image")
    image = Image.open(BytesIO(response.content))
    # Display the image
    image.show()  # Opens the image in the default viewer
else:
    log.error(f"Failed to fetch the image: {response.status_code}")