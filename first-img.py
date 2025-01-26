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

parser = argparse.ArgumentParser(description="Handle POSIX-style prompts in Python")
parser.add_argument("-t", "--text", help="Process as text to image", required=True)
parser.add_argument("-i", "--image", help="Process as image to image.")

# Parse arguments
args = parser.parse_args()

# Create a custom logger
log = logging.getLogger("first_logger")

# Set the logging level
log.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("first.log")

# Set levels for handlers
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

log.addHandler(console_handler)
log.addHandler(file_handler)
# Local file URL
file_url = sys.argv[1]

# Read the file content
log.info("Reading prompt file=" + file_url)

with open(file_url, 'r', encoding='utf-8') as file:
    prompt = json.load(file)
log.debug("prompt=" + str(prompt))

image_path = "scene-office1.png"

log.info("base64_image")
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

prompt["image_prompt"] = base64_image

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

    log.info("Saving the image")
    image.save(sys.argv[2], format="PNG")
else:
    log.error(f"Failed to fetch the image: {response.status_code}")