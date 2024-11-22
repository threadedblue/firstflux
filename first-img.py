from urllib.parse import urlparse
from pathlib import Path
import sys
import os
import requests
import time
from PIL import Image
from io import BytesIO

# Local file URL
file_url = sys.argv[1]

# Parse the URL to extract the path
# current_dir = Path.cwd()
# absolute_path = urlparse(file_url).path
# relative_path = Path(absolute_path).relative_to(absolute_path)

# Read the file content
with open(file_url, 'r', encoding='utf-8') as file:
    prompt = file.read()

print(prompt)

request = requests.post(
    'https://api.bfl.ml/v1/flux-pro-1.1',
    headers={
        'accept': 'application/json',
        'x-key': os.environ.get("BFL_API_KEY"),
        'Content-Type': 'application/json',
    },
    json={
        'prompt': prompt,
        'width': 768,
        'height': 768,
    },
).json()
print(request)
request_id = request["id"]

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
        print("1")
        print(f"Result: {result['result']['sample']}")
 #       export firstjpg="$result['result']['sample']"
        print()
        break
    else:
        print(f"Status: {result['status']}")



# The image URL from the response
image_url = result['result']['sample']

# Fetch the image from the URL
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Load the image into Pillow
    image = Image.open(BytesIO(response.content))
    # Display the image
    image.show()  # Opens the image in the default viewer
else:
    print(f"Failed to fetch the image: {response.status_code}")