import openai
import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()
TOKEN: Final[str] = os.getenv("LITELLM_KEY")

client = openai.OpenAI(
    api_key=TOKEN,
    base_url="http://eldo:4000"
)

# --- Nutritional Variables ---
calories = 1846
protein = 150
fats = 61
carbs = 173

# --- Load the prompt template from the file ---
template_file_path = 'prompt.txt' # Assumes file is in the same directory
prompt_template_string = ""
prompt = "" # Initialize prompt variable

try:
    # Use 'with' to ensure the file is closed automatically
    # Use encoding='utf-8' for better compatibility
    with open(template_file_path, 'r', encoding='utf-8') as f:
        prompt_template_string = f.read()
except FileNotFoundError:
    print(f"Error: Prompt template file not found at '{template_file_path}'")
    print("Please ensure 'meal_prompt_template.txt' is in the same directory as the script.")
    exit() # Exit if the template file is essential and not found
except Exception as e:
    print(f"Error reading prompt template file: {e}")
    exit() # Exit on other file reading errors

# --- Format the template string with current variables ---
if prompt_template_string: # Check if the template was loaded successfully
    try:
        prompt = prompt_template_string.format(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )
    except KeyError as e:
        print(f"Error formatting prompt: Missing placeholder {e} in the template file.")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred during prompt formatting: {e}")
        exit()
else:
    print("Error: Prompt template string is empty. Cannot proceed.")
    exit() # Exit if the template is empty

# --- Make the API Call ---
# Ensure the prompt was successfully created before proceeding
if prompt:
    try:
        print("--- Sending Prompt to API ---")
        # Optional: Print the final formatted prompt to verify
        # print(prompt)
        # print("--------------------------")

        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", # Make sure this model exists on your endpoint
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in creating structured meal plans and shopping lists according to specific nutritional targets and formatting rules."}, # Refined system prompt
                {
                    "role": "user",
                    "content": prompt  # Use the formatted prompt string
                },
            ],
            temperature=0.8 # Set temperature for variability (adjust as needed)
        )

        print("\n--- API Response ---")
        print(completion.choices[0].message.content)
        print("------------------")

    except openai.APIConnectionError as e:
        print(f"Error connecting to OpenAI API at {client.base_url}: {e}")
    except openai.AuthenticationError as e:
        print(f"OpenAI Authentication Error: {e}")
        print("Please check your API key.")
    except openai.RateLimitError as e:
        print(f"OpenAI Rate Limit Exceeded: {e}")
    except openai.APIStatusError as e:
        print(f"OpenAI API Error (Status {e.status_code}): {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred during the API call: {e}")
else:
    print("Prompt generation failed. Cannot make API call.")