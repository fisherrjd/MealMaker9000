import openai
client = openai.OpenAI(
    api_key="sk-_YZAQqYc-qZtAjkjs5wFIA",
    base_url="http://eldo:4000"
)
calories = 1846;
protein = 150;
fats = 61;
carbs = 173;

prompt = (
    # --- Core Goal: Structure vs. Content ---
    f"Generate a 7-day weekly meal plan and a corresponding shopping list. "
    f"Your primary goal is twofold: "
    f"1. **Strict Structural Consistency:** The JSON output formats for both the meal plan and shopping list MUST be *identical* every time, adhering rigidly to the structures defined below. "
    f"2. **Content Variability:** The specific meals generated within the plan SHOULD be *different and varied* each time this prompt is run, while always strictly adhering to the nutritional and ingredient constraints. "

    # --- Constraints for Meal Content ---
    f"Daily Nutritional Targets: Generate meals that collectively meet approximately {calories} calories, {protein}g protein, {carbs}g carbs, and {fats}g fats per day. Calculate these totals accurately for the generated meals. "
    f"Allowed Ingredients: Create diverse meals composed *only* from: chicken, beef, pork, eggs, quinoa, brown rice, steamed vegetables (e.g., broccoli, spinach, bell peppers, carrots). Assume olive oil and basic seasonings (salt, pepper) are usable. "
    f"Excluded Ingredients: Strictly exclude ALL fish and seafood (e.g., Tuna, Salmon, shrimp, etc.). "
    f"Meal Structure: Exactly 3 meals (Breakfast, Lunch, Dinner) and 1 Snack per day for 7 days (Monday to Sunday). "

    # --- Strategy for Variety & Efficiency ---
    "Meal Plan Design Strategy: Prioritize ingredient reuse within the generated week for shopping efficiency (e.g., use chicken bought for Monday also on Wednesday). However, aim for a *different combination* of meals overall compared to previous runs of this prompt. Generate novel meal ideas within the allowed ingredients and macro targets. "

    # --- Output 1: Meal Plan JSON (Strict Format, Variable Content) ---
    "OUTPUT 1: Generate the Meal Plan as a JSON object. "
    "JSON Structure MUST be EXACTLY as follows: Top-level object with keys 'Monday' through 'Sunday'. "
    "Each day's value MUST be an object with EXACTLY these keys: 'Breakfast', 'Lunch', 'Dinner', 'Snack', 'Daily_Calories_Total', 'Daily_Protein', 'Daily_Carbs', 'Daily_Fats'. "
    "Values for meals/snacks MUST be descriptive strings detailing the specific food and estimated portions for *this generated plan* (e.g., 'Omelette (3 eggs) with Bell Peppers', '150g Pork Tenderloin with 1 cup Quinoa and Steamed Green Beans'). "
    "Values for totals MUST be strings starting with 'Approx ' followed by the number and unit (e.g., 'Approx 1980 Kcal', 'Approx 148g', 'Approx 205g', 'Approx 65g'). Calculate these based on the generated meals for the day. DO NOT DEVIATE FROM THIS STRING FORMAT. "
    "Meal Plan Example Snippet (Follow this structure precisely, content will vary): "
    '''
{
  "Monday": {
    "Breakfast": "...", // Different meal description each run
    "Lunch": "...",    // Different meal description each run
    "Dinner": "...",   // Different meal description each run
    "Snack": "...",    // Different meal description each run
    "Daily_Calories_Total": " XXXX Kcal", // Calculated for the generated meals
    "Daily_Protein": " XXXg",    // Calculated for the generated meals
    "Daily_Carbs": " XXXg",      // Calculated for the generated meals
    "Daily_Fats": " XXXg"        // Calculated for the generated meals
  },
  "Tuesday": { // Identical structure, different content
    // ...
  }
  // ... etc. for all 7 days
}
'''

    # --- Output 2: Shopping List JSON (Strict Format, Content based on Output 1) ---
    "\n\nOUTPUT 2: Generate the Shopping List as a *separate* JSON object based *only* on the specific meal plan generated *in Output 1 of this run*. "
    "JSON Structure MUST be EXACTLY as follows: Top-level object with a single key 'Weekly_Shopping_List'. "
    "The value MUST be an object with EXACTLY these category keys (only include a key if items exist for that category in the generated plan): 'Produce', 'Meat_Protein', 'Grains_Pantry', 'Dairy_Eggs', 'Other'. DO NOT INCLUDE empty categories."
    "Under each category key, the value MUST be a JSON array of strings. "
    "Each string MUST list the ingredient and an estimated quantity needed for the week, derived *directly* from the unique meal plan generated above (e.g., 'Chicken Breast (approx 1.0kg)', 'Eggs (1 dozen)', 'Spinach (2 bags)', 'Quinoa (approx 400g)'). Quantities will vary based on the plan. "
    "Shopping List Example (Follow this structure precisely, content/quantities will vary): "
    '''
{
  "Weekly_Shopping_List": {
    "Produce": [ // Items and quantities based on the generated plan
      "<some_food> (approx quantity)",
      "<some_food> (approx quantity)",
      // ... other produce used ...
    ],
    "Meat_Protein": [ // Items and quantities based on the generated plan
      "<some_food> (approx quantity)",
      "<some_food> (approx quantity)",
       // ... other meat used ...
    ],
    "Grains_Pantry": [ // Items and quantities based on the generated plan
      "<some_food> (approx quantity)",
      "<some_food> (approx quantity)",
      // ... other pantry items used ...
    ],
    "Dairy_Eggs": [ // Items and quantities based on the generated plan
      "<some_food> (approx quantity)"
    ],
    "Other": [
      "Olive Oil (check pantry)", // Static items can remain
      "Salt, Pepper, Spices (check pantry)"
    ]
  }
}
'''
    # --- Final Instructions ---
    "Ensure BOTH JSON outputs are provided, are valid, and strictly follow the specified structures. Prioritize generating a *new and different* set of meals adhering to all constraints each time. Do not add commentary outside the JSON outputs."
)

# calories = input("Please enter Calories: ")
# protein = input("Please enter Protein: ")
# fats = input("Please enter Fats: ")
# carbs = input("Please enter Carbs: ")

completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {"role": "system", "content": "Talk like a Nutritionist to help the user create a meal plan!"},
        {
            "role": "user",
            "content": prompt
        },
    ],
)

print(completion.choices[0].message.content)