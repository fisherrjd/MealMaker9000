import openai
import os
from dotenv import load_dotenv
from typing import Final, Optional
import json

# --- Load Environment Variables ---
load_dotenv()
TOKEN: Final[Optional[str]] = os.getenv("SCOUT_KEY")
if not TOKEN:
    print("Error: SCOUT_KEY environment variable not set.")
    exit(1) # Exit if the essential API key is missing

# --- Constants ---
TEMPLATE_FILE_PATH: Final[str] = 'prompt.txt' # Assumes file is in the same directory
API_BASE_URL: Final[str] = "http://eldo:4000"
API_MODEL: Final[str] = "meta-llama/llama-4-scout-17b-16e-instruct"

# --- Initialize OpenAI Client (once) ---
try:
    client = openai.OpenAI(
        api_key=TOKEN,
        base_url=API_BASE_URL
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit(1)


def generate_meal_plan_json(
    prompt_template_path: str = TEMPLATE_FILE_PATH
) -> Optional[str]:
    """
    Generates a meal plan based on nutritional macros using an OpenAI-compatible API.

    Args:
        prompt_template_path: Path to the prompt template file.

    Returns:
        A string containing the first JSON object (meal plan) from the API response,
        or None if an error occurred during generation or processing.
    """
    # --- Load the prompt template ---
    try:
        with open(prompt_template_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print(f"Error: Prompt template file not found at '{prompt_template_path}'")
        return None
    except Exception as e:
        print(f"Error reading prompt template file '{prompt_template_path}': {e}")
        return None


    # --- Make the API Call ---
    try:
        completion = client.chat.completions.create(
            model=API_MODEL,
            messages=[
                 {"role": "system", "content": "You are a helpful assistant skilled in creating structured meal plans according to specific nutritional targets and formatting rules. You MUST output the meal plan as a valid JSON object FIRST, followed potentially by other text or JSON."}, # Adjusted system prompt slightly
                {
                    "role": "user",
                    "content": prompt_template
                },
            ],
            temperature=0.7
        )
        response_content = completion.choices[0].message.content
        print(response_content)


    except openai.APIConnectionError as e:
        print(f"Error connecting to API at {client.base_url}: {e}")
        return None
    # ... (other specific exception handling remains the same) ...
    except Exception as e:
        print(f"An unexpected error occurred during the API call: {e}")
        return None

    if not response_content:
        print("Error: API returned an empty response.")
        return None




# --- Example Usage (demonstrates calling the function) ---
if __name__ == "__main__":
    # Call the function - it will return the string or None
    meal_plan_json_string = generate_meal_plan_json()
