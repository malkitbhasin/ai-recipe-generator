#!/usr/bin/env python
# coding: utf-8

import os
import base64
import io
from dotenv import load_dotenv
from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from parse_ingredients import parse_ingredients_with_openai

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set")

# Initialize the Gemini API client
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  # or gemini-1.5-pro

def image_url(img):
    """Convert an image to a base64 URL."""
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode("utf-8")

def generate_recipe(prompt, img):
    """Generate a recipe using the Gemini API."""
    message = HumanMessage(content=[
        {'type': 'text', 'text': prompt},
        {'type': 'image_url', 'image_url': image_url(img)}
    ])
    response = model.stream([message])

    # Collect and return the response
    buffer = []
    for chunk in response:
        buffer.append(chunk.content)
    return ''.join(buffer)


# Create a text prompt
prompt = 'Provide an example recipe for the cooked food in the image'

# Load an image with PIL
img = Image.open(os.path.join(os.path.dirname(__file__), "../baked_goods_1.jpg"))

# Call the Gemini API using LangChain
recipe = generate_recipe(prompt, img)
print(recipe)

ingradients = parse_ingredients_with_openai(recipe)
print(ingradients.to_string(index=False))



