from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Load the seating plan data
try:
    seating_data = pd.read_csv('seating plan2.csv')  # Ensure the CSV file path is correct
    seating_data.columns = seating_data.columns.str.strip().str.lower()  # Clean and standardize column names
    seating_data['first name'] = seating_data['first name'].str.strip().str.lower()  # Standardize names
    seating_data['family name'] = seating_data['family name'].str.strip().str.lower()
    print("Loaded columns:", seating_data.columns)  # Debug: Check the available columns
except FileNotFoundError:
    print("Error: CSV file not found. Please check the file name and path.")
    exit()

@app.route('/')
def welcome():
    # Render the welcome page
    return render_template('welcome.html')

@app.route('/table_check', methods=['GET', 'POST'])
def table_check():
    if request.method == 'POST':
        # Get the entered first and family names from the form
        first_name = request.form.get('First_Name').strip().lower()
        family_name = request.form.get('Family_Name').strip().lower()

        # Search for matching rows in the CSV data
        matching_row = seating_data[
            (seating_data['first name'] == first_name) & 
            (seating_data['family name'] == family_name)
        ]

        if not matching_row.empty:
            # Extract the table number
            table_number = matching_row.iloc[0]['table number'].strip().lower()

            # Check if the table number indicates the friends zone
            is_friends_zone = table_number == 'friends zone'

            # Debug: Check the is_friends_zone status
            print(f"Guest found: {first_name} {family_name}, Table Number: {table_number}, Is Friends Zone: {is_friends_zone}")

            return jsonify({'success': True, 'table_number': table_number, 'is_friends_zone': is_friends_zone})
        else:
            # Debug: Print when no match is found
            print(f"No match found for: {first_name} {family_name}")
            # Return an error message if names are not found
            return jsonify({'success': False})

    # Render the table check page
    return render_template('table_check.html')

if __name__ == '__main__':
    app.run(debug=True)
