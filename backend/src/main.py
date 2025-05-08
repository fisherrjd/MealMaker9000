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
    exit(1)

# --- Constants ---
TEMPLATE_FILE_PATH: Final[str] = 'prompt_v2.txt'
API_BASE_URL: Final[str] = "http://eldo:4000"
API_MODEL: Final[str] = "meta-llama/llama-4-scout-17b-16e-instruct"

# --- Initialize OpenAI Client ---
try:
    client = openai.OpenAI(
        api_key=TOKEN,
        base_url=API_BASE_URL
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit(1)

# --- Structured Tool Definition ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_structured_meal_plan_and_shopping_list",
            "description": "Generates a 7-day meal plan and shopping list based on allowed ingredients. Strict JSON structure.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Meal_Ideas": {
                        "type": "object",
                        "properties": {
                            "Monday": {
                                "type": "object",
                                "properties": {
                                    "Breakfast": {"type": "string"},
                                    "Lunch": {"type": "string"},
                                    "Dinner": {"type": "string"},
                                    "Snack": {"type": "string"}
                                },
                                "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                            },
                            "Tuesday": {
                                "type": "object",
                                "properties": {
                                    "Breakfast": {"type": "string"},
                                    "Lunch": {"type": "string"},
                                    "Dinner": {"type": "string"},
                                    "Snack": {"type": "string"}
                                },
                                "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                            },
                            "Wednesday": {
                                "type": "object",
                                "properties": {
                                    "Breakfast": {"type": "string"},
                                    "Lunch": {"type": "string"},
                                    "Dinner": {"type": "string"},
                                    "Snack": {"type": "string"}
                                },
                                "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                            },
                            "Thursday": {
                                "type": "object",
                                "properties": {
                                    "Breakfast": {"type": "string"},
                                    "Lunch": {"type": "string"},
                                    "Dinner": {"type": "string"},
                                    "Snack": {"type": "string"}
                                },
                                "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                            },
                            "Friday": {
                                "type": "object",
                                "properties": {
                                    "Breakfast": {"type": "string"},
                                    "Lunch": {"type": "string"},
                                    "Dinner": {"type": "string"},
                                    "Snack": {"type": "string"}
                                },
                                "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                            },
                            "Saturday": {
                                "type": "object",
                                "properties": {
                                    "Breakfast": {"type": "string"},
                                    "Lunch": {"type": "string"},
                                    "Dinner": {"type": "string"},
                                    "Snack": {"type": "string"}
                                },
                                "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                            },
                            "Sunday": {
                                "type": "object",
                                "properties": {
                                    "Breakfast": {"type": "string"},
                                    "Lunch": {"type": "string"},
                                    "Dinner": {"type": "string"},
                                    "Snack": {"type": "string"}
                                },
                                "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                            }
                        },
                        "required": [
                            "Monday", "Tuesday", "Wednesday",
                            "Thursday", "Friday", "Saturday", "Sunday"
                        ]
                    },
                    "Weekly_Shopping_List": {
                        "type": "object",
                        "properties": {
                            "Produce": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "Meat_Protein": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "Dairy_Eggs": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "Pantry": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "additionalProperties": False
                    }
                },
                "required": ["Meal_Ideas", "Weekly_Shopping_List"]
            }
        }
    }
]



def generate_meal_plan_json(
    prompt_template_path: str = TEMPLATE_FILE_PATH
) -> Optional[dict]:
    """
    Generates a 7-day meal plan and shopping list using structured output.
    Returns structured dict, or None on error.
    """
    try:
        with open(prompt_template_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
    except Exception as e:
        print(f"Error loading prompt: {e}")
        return None

    try:
        completion = client.chat.completions.create(
            model=API_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a structured meal planner that outputs JSON following the exact format required. "
                        "Always vary the meals, never vary the breakfast, and never include disallowed ingredients. "
                        "Output both 'Meal_Ideas' and 'Weekly_Shopping_List' as JSON keys."
                    )
                },
                {"role": "user", "content": prompt_template}
            ],
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )

        tool_calls = completion.choices[0].message.tool_calls
        if not tool_calls:
            print("No structured output returned.")
            return None

        arguments_str = tool_calls[0].function.arguments
        structured_output = json.loads(arguments_str)

        # Optional: print both parts
        print("\n=== Meal Plan ===")
        print(json.dumps(structured_output["Meal_Ideas"], indent=2))
        print("\n=== Shopping List ===")
        print(json.dumps({"Weekly_Shopping_List": structured_output["Weekly_Shopping_List"]}, indent=2))

        return structured_output

    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        return None
    except openai.APIConnectionError as e:
        print(f"API connection error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# --- Run Example ---
if __name__ == "__main__":
    generate_meal_plan_json()
