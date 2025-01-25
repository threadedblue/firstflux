#!/usr/bin/env pytnon

from urllib.parse import urlparse
from pathlib import Path
import sys
import os
import requests
import time
from PIL import Image
from io import BytesIO
import logging

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

# Local file URL
file_url = sys.argv[1]

# Parse the URL to extract the path
# current_dir = Path.cwd()
# absolute_path = urlparse(file_url).path
# relative_path = Path(absolute_path).relative_to(absolute_path)

# Read the file content
log.info("Reading prompt file=" + file_url)

with open(file_url, 'r', encoding='utf-8') as file:
    prompt = file.read()

log.debug(prompt)

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