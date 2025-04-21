import os
import logging
from dotenv import load_dotenv
from typing import List
import pandas as pd
from pydantic import BaseModel, Field
from openai import OpenAI

# --------------------------------------------------------------
# Setup
# --------------------------------------------------------------

# Load environment variables from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# --------------------------------------------------------------
# Define Pydantic models for structured output
# --------------------------------------------------------------

class Ingredient(BaseModel):
    quantity: str = Field(description="Amount of the ingredient, e.g. '2 cups'")
    ingredient: str = Field(description="Name of the ingredient, e.g. 'flour'")

class IngredientsList(BaseModel):
    ingredients: List[Ingredient]

# --------------------------------------------------------------
# Function to parse ingredients using OpenAI
# --------------------------------------------------------------

def parse_ingredients_with_openai(recipe_text: str) -> pd.DataFrame:
    logger.info("Parsing ingredients from recipe")
    
    prompt = f"""
Extract the ingredients from the following recipe and return them as a JSON object 
with a single field "ingredients", which is a list of objects with 'quantity' and 'ingredient' keys.

Recipe:
{recipe_text}
"""

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format=IngredientsList,
        )
        parsed: IngredientsList = response.choices[0].message.parsed
        logger.info("Ingredient parsing successful")
        return pd.DataFrame([i.dict() for i in parsed.ingredients])

    except Exception as e:
        logger.error(f"Failed to parse ingredients: {e}")
        raise ValueError("Failed to parse ingredients from OpenAI response") from e

# --------------------------------------------------------------
# Example usage
# --------------------------------------------------------------

def main():
    recipe_output = """
2 cups of flour
1 cup of sugar
1/2 cup of butter
3 eggs
1 teaspoon of vanilla extract
"""

    ingredients_df = parse_ingredients_with_openai(recipe_output)
    print(ingredients_df.to_string(index=False))

if __name__ == "__main__":
    main()
