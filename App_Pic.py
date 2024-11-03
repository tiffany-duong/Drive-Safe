import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def download_image(filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print("Error downloading image from URL:", url)

def filename_from_input(prompt):
    # Remove all non-alphanumeric characters from the prompt except spaces.
    alphanum = ""
    for character in prompt:
        if character.isalnum() or character == " ":
            alphanum += character
    # Split the alphanumeric prompt into words.
    alphanum_split = alphanum.split()
    if len(alphanum_split) > 3:
        alphanum_split = alphanum_split[:3]
    # Join the words with underscores and return the result.
    return "images/" + "_".join(alphanum_split)

def get_image(prompt, model="dall-e-2"):
    n = 2  # Number of images to generate

    # Generate images using new API format
    image_response = client.images.generate(
        model=model,
        prompt=prompt,
        n=n,
        size="1024x1024"
    )

    # Ensure images directory exists
    os.makedirs("images", exist_ok=True)

    # Save images and return response
    for i in range(n):
        filename = filename_from_input(prompt) + "_" + str(i + 1) + ".png"
        download_image(filename, image_response.data[i].url)

    return image_response