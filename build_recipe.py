#!/usr/bin/env python
# coding: utf-8

# # Baking with the Gemini API
# 
# To get started, [get an API key](https://g.co/ai/idxGetGeminiKey) and replace the word `TODO` below with your API key:

# In[1]:

import os
import base64
import io
from dotenv import load_dotenv
from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
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


# Once you're done, create a text prompt here:

# In[2]:


prompt = 'Provide an example recipe for the baked goods in the image'


# And load an image with PIL:

# In[3]:


img = Image.open('baked_goods_1.jpg')
# img = Image.open('baked_goods_2.jpg')
# img = Image.open('baked_goods_3.jpg')
img


# And finally, call the Gemini API using LangChain. [See the docs](https://github.com/langchain-ai/langchain/blob/master/libs/partners/google-genai/langchain_google_genai/__init__.py)

# In[4]:


recipe = generate_recipe(prompt, img)
print(recipe)

