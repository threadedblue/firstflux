from urllib.parse import urlparse
import os
import requests
import time
# Local file URL
file_url = "file:///$1"

# Parse the URL to extract the path
file_path = urlparse(file_url).path

# Read the file content
with open(file_path, 'r', encoding='utf-8') as file:
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
        export firstjpg="$result['result']['sample']"
        print()
        break
    else:
        print(f"Status: {result['status']}")