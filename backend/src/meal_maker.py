from flask import Flask, request, jsonify

# 1. Initialize Flask App
app = Flask(__name__)

# 2. Define the Endpoint
@app.route('/submit-macros', methods=['POST'])
def handle_macros():
    """
    Receives macronutrient data (calories, protein, carbs, fats)
    via JSON POST request and returns the received data.

    Expects JSON body like:
    {
        "calories": 2000,
        "protein": 150,
        "carbs": 250,
        "fats": 60
    }
    """
    # 3. Get JSON data from the request
    # request.is_json ensures the Content-Type header is application/json
    if not request.is_json:
        return jsonify({"error": "Invalid request: Content-Type must be application/json"}), 415 # Unsupported Media Type

    data = request.get_json()

    # 4. Basic Input Validation: Check if data is a dictionary
    if not isinstance(data, dict):
         return jsonify({"error": "Invalid request: JSON data must be an object"}), 400 # Bad Request

    # 5. Extract specific fields and perform validation
    required_fields = ["calories", "protein", "carbs", "fats"]
    received_data = {}
    missing_fields = []
    invalid_fields = [] # To store fields with non-numeric or negative values

    for field in required_fields:
        value = data.get(field) # Use .get() to avoid KeyError if field is missing

        if value is None: # Check if field is present
            missing_fields.append(field)
        else:
            # Validate Data Type (check if numeric) and Value (non-negative)
            try:
                # Convert to float to allow decimals, also handles integers
                numeric_value = float(value)
                if numeric_value < 0:
                    invalid_fields.append(f"{field}: value cannot be negative ({value})")
                else:
                    received_data[field] = numeric_value # Store the validated numeric value
            except (ValueError, TypeError):
                invalid_fields.append(f"{field}: value must be numeric ({value})")

    # 6. Handle Validation Errors
    errors = {}
    if missing_fields:
        errors["missing_fields"] = missing_fields
    if invalid_fields:
        errors["invalid_type_or_value"] = invalid_fields

    if errors:
        # Return 400 Bad Request with details about the errors
        return jsonify({"error": "Validation failed", "details": errors}), 400

    # 7. Prepare and Return Success Response
    # If all validations pass, return the received (and potentially type-converted) data
    response = {
        "message": "Data received successfully",
        "received_data": received_data # Pass back the validated data
    }

    cals = received_data['calories']
    prot = received_data['protein']
    carb = received_data['carbs']
    fat = received_data['fats']
    print(f"calories:{cals}")
    return jsonify(response), 200 # 200 OK

# 8. Run the App
if __name__ == '__main__':
    # debug=True enables auto-reloading and provides detailed error pages
    # Use a different port like 5001 if 5000 is in use
    app.run(debug=True, port=5001)