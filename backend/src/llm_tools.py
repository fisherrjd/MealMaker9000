# llm_tools.py

MEAL_PLANNER_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "generate_structured_meal_plan_and_shopping_list",
            "description": "Generates a single day meal plan and shopping list based on allowed ingredients. Strict JSON structure.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Daily_Meal_Plan": {
                        "type": "object",
                        "description": "The meal plan for a single day.",
                        "properties": {
                            "Breakfast": {"type": "string", "description": "Description of the breakfast meal."},
                            "Lunch": {"type": "string", "description": "Description of the lunch meal."},
                            "Dinner": {"type": "string", "description": "Description of the dinner meal."},
                            "Snack": {"type": "string", "description": "Description of the snack."}
                        },
                        "required": ["Breakfast", "Lunch", "Dinner", "Snack"]
                    },
                    "Weekly_Shopping_List": { # Kept name, but content will be for the day
                        "type": "object",
                        "description": "Shopping list for the ingredients needed for the day's meals.",
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
                        "additionalProperties": False # Ensures no extra categories in shopping list
                    }
                },
                "required": ["Daily_Meal_Plan", "Weekly_Shopping_List"] # Updated required top-level keys
            }
        }
    }
]
