# main_script.py

import openai
import os
from dotenv import load_dotenv
from typing import Final, Optional, List # Added List for dynamic prompts later
import json

# Import the tool definition from your new file
from llm_tools import MEAL_PLANNER_TOOL # Or 'from llm_tools import tools' if you named it that

# --- Load Environment Variables ---
load_dotenv()
TOKEN: Final[Optional[str]] = os.getenv("SCOUT_KEY")
if not TOKEN:
    print("Error: SCOUT_KEY environment variable not set.")
    exit(1)

# --- Constants ---
TEMPLATE_FILE_PATH: Final[str] = 'prompt_v2.txt'
API_BASE_URL: Final[str] = "https://litellm.jade.rip/" # Replace if needed
API_MODEL: Final[str] = "meta-llama/llama-4-scout-17b-16e-instruct" # Replace if needed

# --- Initialize OpenAI Client ---
try:
    client = openai.OpenAI(
        api_key=TOKEN,
        base_url=API_BASE_URL
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit(1)

# The 'tools' variable below will now use the imported definition
# tools = MEAL_PLANNER_TOOL # This line is effectively handled by using MEAL_PLANNER_TOOL directly in the API call

def generate_meal_plan_template():
    print("TODO: generate_meal_plan_template")


def call_openAI():
    print("TODO: call LLM to generate meal")

# --- Run Example ---
if __name__ == "__main__":
    generate_meal_plan_template()
    call_openAI()