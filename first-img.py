
import os
import requests
import time


request = requests.post(
    'https://api.bfl.ml/v1/flux-pro-1.1',
    headers={
        'accept': 'application/json',
        'x-key': os.environ.get("BFL_API_KEY"),
        'Content-Type': 'application/json',
    },
    json={
        'prompt': 'Realistic Cartoon, A portrait of a woman, blue eyes, blonde hair, wearing a yellow sundress with white polka dots',
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