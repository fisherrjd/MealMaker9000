import openai
import os
from dotenv import load_dotenv
from typing import Final
import json

load_dotenv()
TOKEN: Final[str] = os.getenv("SCOUT_KEY")

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
prompt = "" # Initialize prompt variable

try:
    # Use 'with' to ensure the file is closed automatically
    # Use encoding='utf-8' for better compatibility
    with open(template_file_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
except FileNotFoundError:
    print(f"Error: Prompt template file not found at '{template_file_path}'")
    print("Please ensure 'meal_prompt_template.txt' is in the same directory as the script.")
    exit() # Exit if the template file is essential and not found
except Exception as e:
    print(f"Error reading prompt template file: {e}")
    exit() # Exit on other file reading errors

# --- Format the template string with current variables ---
if prompt_template: # Check if the template was loaded successfully
    try:
        prompt = prompt_template.format(
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

# Load the JSON data
response = completion.choices[0].message.content

# Remove any extra newline characters or whitespace
print("\n\nStripping Output...")
ai_output = response.strip().replace('```json', '').replace('```', '')

json1_str = None
json2_str = None

try:
    # Prepare the input string
    cleaned_input = ai_output.strip()
    decoder = json.JSONDecoder()

    # Find the end of the first JSON object
    # raw_decode returns (python_object, index_where_parsing_stopped)
    _, end_pos1 = decoder.raw_decode(cleaned_input)

    # Extract the first JSON string
    json1_str = cleaned_input[:end_pos1]

    # Assume the rest of the string (after stripping whitespace) is the second JSON
    json2_str = cleaned_input[end_pos1:].strip()

    # Basic validation: Check if the second part looks like a JSON object
    if not (json2_str.startswith('{') and json2_str.endswith('}')):
        print("Warning: Second part doesn't look like a standard JSON object.")
        # Decide if you want to nullify json2_str here based on strictness
        # json2_str = None # Uncomment if strict validation is needed

except (json.JSONDecodeError, IndexError) as e:
    print(f"Error processing the input: {e}")
    print("Could not reliably split the JSON objects.")
    json1_str = None # Ensure variables are None on error
    json2_str = None
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    json1_str = None
    json2_str = None


# --- Output the results ---
if json1_str:
    print("--- JSON 1 ---")
    print(json1_str)

if json2_str:
    print("\n--- JSON 2 ---")
    print(json2_str)

elif json1_str and not json2_str:
     print("\nSuccessfully extracted JSON 1, but failed to extract JSON 2.")

elif not json1_str:
     print("\nFailed to extract any JSON objects.")