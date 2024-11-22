from PIL import Image
import requests
from io import BytesIO

# The image URL from the response
image_url = sys.argv[1]

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
