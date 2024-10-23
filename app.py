from flask import Flask, request, render_template
import pandas as pd
import os
from filelock import FileLock, Timeout

app = Flask(__name__)

# Define the path to your Excel file and the lock file
EXCEL_FILE = "data.xlsx"
LOCK_FILE = "data.lock"

# Check if the Excel file exists, if not, create it with headers
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Email", "Age", "DOB", "Program of Study", "Graduation Year", "Phone Number"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def form():
    return render_template('form.html')  # Load the HTML form

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    dob = request.form['dob']
    program = request.form['program']
    graduation_year = request.form['graduation_year']
    phone = request.form['phone']

    # File locking to prevent concurrent writes
    lock = FileLock(LOCK_FILE, timeout=10)  # Wait for 10 seconds before timing out

    try:
        with lock:
            # Load the Excel file into a DataFrame
            df = pd.read_excel(EXCEL_FILE)

            # Append new data to the DataFrame
            new_data = pd.DataFrame({
                'Name': [name],
                'Email': [email],
                'Age': [age],
                'DOB': [dob],
                'Program of Study': [program],
                'Graduation Year': [graduation_year],
                'Phone Number': [phone]
            })

            df = pd.concat([df, new_data], ignore_index=True)

            # Save the updated DataFrame back to Excel
            df.to_excel(EXCEL_FILE, index=False)

        return "Form submitted successfully and data saved to Excel!"

    except Timeout:
        return "The Excel file is currently being used. Please try again later."

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)

