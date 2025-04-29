import json
from tabulate import tabulate

def display_json_data(json_data):
    print("## Meal Plan Data")
    print("----------------")

    for day, meals in json_data.items():
        print(f"### {day}")
        table = []

        for meal_name, meal_data in meals.items():
            if meal_name != "Totals":
                table.append([meal_name, meal_data["description"], meal_data["calories"], meal_data["protein"], meal_data["carbohydrates"], meal_data["fats"]])

        print(tabulate(table, headers=["Meal", "Description", "Calories", "Protein", "Carbohydrates", "Fats"], tablefmt="fancy_grid"))

        totals = meals["Totals"]
        print(f"**Totals: {totals['calories']} calories, {totals['protein']}g protein, {totals['carbohydrates']}g carbohydrates, {totals['fats']}g fats")
        print()

def main():
    with open('meal_plan.json', 'r') as f:
        json_data = json.load(f)

    display_json_data(json_data)

if __name__ == "__main__":
    main()