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
    calories: int,
    protein: int,
    fats: int,
    carbs: int,
    prompt_template_path: str = TEMPLATE_FILE_PATH
) -> Optional[str]:
    """
    Generates a meal plan based on nutritional macros using an OpenAI-compatible API.

    Args:
        calories: Target daily calories.
        protein: Target daily protein (in grams).
        fats: Target daily fat (in grams).
        carbs: Target daily carbohydrates (in grams).
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

    if not prompt_template:
        print("Error: Prompt template string is empty. Cannot proceed.")
        return None

    # --- Format the prompt ---
    try:
        prompt = prompt_template.format(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )
    except KeyError as e:
        print(f"Error formatting prompt: Missing placeholder {e} in the template file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during prompt formatting: {e}")
        return None

    # --- Make the API Call ---
    try:
        print(f"--- Sending Prompt to API for {calories}kcal, {protein}p, {fats}f, {carbs}c ---")
        completion = client.chat.completions.create(
            model=API_MODEL,
            messages=[
                 {"role": "system", "content": "You are a helpful assistant skilled in creating structured meal plans according to specific nutritional targets and formatting rules. You MUST output the meal plan as a valid JSON object FIRST, followed potentially by other text or JSON."}, # Adjusted system prompt slightly
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0.7
        )
        response_content = completion.choices[0].message.content

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

    print("--- Processing API Response for Combined JSON ---")

    # --- Clean the input string ---
    # Remove markdown, strip leading/trailing whitespace
    cleaned_input = response_content.strip().replace('```json', '').replace('```', '').strip()

    # Find the start of the first JSON object
    start_index = cleaned_input.find('{')
    if start_index == -1:
         print("Error: Could not find the start of any JSON object ('{') in the response.")
         return None
    # Work with the string starting from the first '{'
    relevant_input = cleaned_input[start_index:]

    decoder = json.JSONDecoder()
    data1 = None
    data2 = None
    combined_data = {}

    try:
        # --- Process and Parse the First JSON ---
        # raw_decode finds the end of the first valid JSON structure
        # It returns the parsed Python object and the index where parsing stopped
        obj1, end_pos1 = decoder.raw_decode(relevant_input)
        data1 = obj1 # Store the parsed first dictionary
        print("--- Successfully parsed first JSON object ---")

        # --- Process and Parse the Second JSON ---
        # Get the rest of the string after the first JSON
        remaining_input = relevant_input[end_pos1:].strip()

        if not remaining_input:
            print("Warning: No remaining content found after the first JSON object.")
            # Decide if returning only the first object is acceptable
            # return data1 # Uncomment if returning only the first is ok
            print("Error: Expected a second JSON object, but found none.")
            return None # Or return None/error if two are strictly required

        # Find the start of the second JSON object in the remainder
        start_index_2 = remaining_input.find('{')
        if start_index_2 == -1:
             print("Error: Could not find the start ('{') of the second JSON object.")
             print("Remaining text starts with:", remaining_input[:50])
             return None

        # Decode the second JSON object starting from its '{'
        obj2, _ = decoder.raw_decode(remaining_input[start_index_2:]) # We don't need end_pos2 here
        data2 = obj2 # Store the parsed second dictionary
        print("--- Successfully parsed second JSON object ---")

        # --- Combine the Dictionaries ---
        # Create a new dictionary and update it. This handles potential key collisions
        # If keys are guaranteed unique (like the example), this is fine.
        # If keys might overlap, consider a nested structure:
        # combined_data = {'part1': data1, 'part2': data2}
        if data1:
            combined_data.update(data1)
        if data2:
            combined_data.update(data2) # data2 keys will overwrite data1 keys if they collide

        if not combined_data:
             print("Error: Failed to parse any data into the combined dictionary.")
             return None

        print("--- Successfully combined data from both JSON objects ---")
        # <<< --- THIS IS THE COMBINED DICTIONARY TO RETURN --- >>>
        return combined_data

    except json.JSONDecodeError as e:
        # Provide context about where the error likely happened
        if data1 is None: # Error likely in the first JSON
             print(f"Error decoding the first JSON object: {e}")
             print(f"Nearby text: {relevant_input[max(0, e.pos-20):e.pos+20]}")
        elif data2 is None: # Error likely in the second JSON
             print(f"Error decoding the second JSON object: {e}")
             print(f"Nearby text (in remaining part): {remaining_input[max(0, e.pos-20):e.pos+20]}")
        else: # Should not happen if logic is correct, but catch anyway
             print(f"An unexpected JSON decoding error occurred: {e}")
        return None
    except IndexError as e:
         print(f"Error processing string indices, likely due to unexpected format: {e}")
         return None
    except Exception as e:
        print(f"An unexpected error occurred during JSON processing: {e}")
        return None


# --- Example Usage (demonstrates calling the function) ---
if __name__ == "__main__":
    target_calories = 1900
    target_protein = 155
    target_fats = 65
    target_carbs = 175

    print(f"Requesting meal plan for: {target_calories} Cals, {target_protein}g P, {target_fats}g F, {target_carbs}g C")

    # Call the function - it will return the string or None
    meal_plan_json_string = generate_meal_plan_json(
        calories=target_calories,
        protein=target_protein,
        fats=target_fats,
        carbs=target_carbs
    )

    if meal_plan_json_string:
        print("\n--- Returned Meal Plan JSON String ---")
        print(meal_plan_json_string)
    else:
        print("\n--- Function failed to return a valid JSON string ---")