const mealPlanData = {
    "Monday": {
        "Breakfast": "Scrambled Eggs (2 eggs) with Spinach and Bell Peppers",
        "Lunch": "Grilled Chicken Breast (150g) with Steamed Broccoli and Carrots",
        "Dinner": "Beef Stir-Fry (120g) with Onions, Bell Peppers, and Brown Rice (1 cup)",
        "Snack": "Omelette (1 egg) with Spinach",
        "Daily_Calories_Total": " 1846 Kcal",
        "Daily_Protein": " 150g",
        "Daily_Carbs": " 173g",
        "Daily_Fats": " 61g"
    },
    "Tuesday": {
        "Breakfast": "Beef and Vegetable Omelette (2 eggs, 50g beef) with Toast",
        "Lunch": "Chicken and Vegetable Soup (200g chicken, 1 cup mixed vegetables)",
        "Dinner": "Grilled Chicken Breast (150g) with Roasted Onions and Bell Peppers",
        "Snack": "Hard-Boiled Egg (1 egg)",
        "Daily_Calories_Total": " 1846 Kcal",
        "Daily_Protein": " 150g",
        "Daily_Carbs": " 173g",
        "Daily_Fats": " 61g"
    },
    "Wednesday": {
        "Breakfast": "Chicken and Spinach Scramble (2 eggs, 100g chicken)",
        "Lunch": "Beef and Vegetable Stir-Fry (120g beef, 1 cup mixed vegetables) with Brown Rice",
        "Dinner": "Baked Chicken Thigh (150g) with Steamed Carrots and Green Beans",
        "Snack": "Yogurt and Bell Pepper Slices (not exceeding daily nutritional targets)",
        "Daily_Calories_Total": " 1846 Kcal",
        "Daily_Protein": " 150g",
        "Daily_Carbs": " 173g",
        "Daily_Fats": " 61g"
    },
    "Thursday": {
        "Breakfast": "Omelette (2 eggs) with Mushrooms and Spinach",
        "Lunch": "Grilled Chicken Breast (150g) with Mixed Greens Salad and Olive Oil Dressing",
        "Dinner": "Beef and Onion Meatballs (120g) with Steamed Broccoli",
        "Snack": "Cottage Cheese and Cucumber Slices (not exceeding daily nutritional targets)",
        "Daily_Calories_Total": " 1846 Kcal",
        "Daily_Protein": " 150g",
        "Daily_Carbs": " 173g",
        "Daily_Fats": " 61g"
    },
    "Friday": {
        "Breakfast": "Breakfast Burrito (2 eggs, 50g beef, Bell Peppers)",
        "Lunch": "Chicken Caesar Salad (200g chicken, 1 cup romaine lettuce)",
        "Dinner": "Grilled Chicken Breast (150g) with Roasted Vegetables",
        "Snack": "Hard-Boiled Egg (1 egg) and Carrot Sticks",
        "Daily_Calories_Total": " 1846 Kcal",
        "Daily_Protein": " 150g",
        "Daily_Carbs": " 173g",
        "Daily_Fats": " 61g"
    },
    "Saturday": {
        "Breakfast": "Beef and Spinach Frittata (2 eggs, 50g beef)",
        "Lunch": "Chicken and Vegetable Wrap (200g chicken, 1 cup mixed vegetables)",
        "Dinner": "Baked Chicken Thigh (150g) with Quinoa (replaced with Brown Rice for variety) and Steamed Green Beans",
        "Snack": "Cottage Cheese and Cucumber (adjusted for daily targets)",
        "Daily_Calories_Total": " 1846 Kcal",
        "Daily_Protein": " 150g",
        "Daily_Carbs": " 173g",
        "Daily_Fats": " 61g"
    },
    "Sunday": {
        "Breakfast": "Omelette (2 eggs) with Bell Peppers and Onions",
        "Lunch": "Grilled Chicken Breast (150g) with Steamed Broccoli and Brown Rice",
        "Dinner": "Beef Stir-Fry (120g) with Mixed Vegetables and Brown Rice",
        "Snack": "Yogurt with Spinach and Bell Pepper (within daily limits)",
        "Daily_Calories_Total": " 1846 Kcal",
        "Daily_Protein": " 150g",
        "Daily_Carbs": " 173g",
        "Daily_Fats": " 61g"
    }
};

// Helper function to format summary keys nicely
function formatSummaryKey(key) {
    return key.replace('Daily_', '').replace('_Total', '').replace(/_/g, ' ');
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('mealPlanContainer');
    const daysOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const mealKeys = ["Breakfast", "Lunch", "Dinner", "Snack"];

    if (!container) {
        console.error("Error: Container element #mealPlanContainer not found!");
        return;
    }

    daysOrder.forEach(day => {
        const dayData = mealPlanData[day];
        if (!dayData) return; // Skip if data for a day is missing

        // Create card container
        const dayCard = document.createElement('div');
        dayCard.classList.add('day-card');

        // Day Title
        const title = document.createElement('h2');
        title.textContent = day;
        dayCard.appendChild(title);

        // Meals Section
        const mealsTitle = document.createElement('h3');
        mealsTitle.textContent = 'Meals';
        dayCard.appendChild(mealsTitle);

        const mealsList = document.createElement('ul');
        mealKeys.forEach(mealKey => {
            if (dayData[mealKey]) { // Check if the meal exists for the day
                const listItem = document.createElement('li');
                listItem.innerHTML = `<strong>${mealKey}:</strong> ${dayData[mealKey]}`;
                mealsList.appendChild(listItem);
            }
        });
        dayCard.appendChild(mealsList);

        // Summary Section
        const summaryTitle = document.createElement('h3');
        summaryTitle.textContent = 'Daily Summary';
        dayCard.appendChild(summaryTitle);

        const summaryList = document.createElement('ul');
        Object.keys(dayData).forEach(key => {
            // Only include keys that are NOT meals
            if (!mealKeys.includes(key)) {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<strong>${formatSummaryKey(key)}:</strong> ${dayData[key]}`;
                summaryList.appendChild(listItem);
            }
        });
        dayCard.appendChild(summaryList);


        // Append the card to the main container
        container.appendChild(dayCard);
    });
});