from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the merged quiz results CSV into a DataFrame
df = pd.read_csv('Madrassa_Quiz_Total - Others-Total Sheet.csv')
# Sort the DataFrame by 'Total New Score' in descending order
df.sort_values(by='Total New Score', ascending=False, inplace=True)

# Add a Serial Number (Sr. No.) column
df.reset_index(drop=True, inplace=True)
df['Rank'] = df.index + 1
# Reorder columns to make 'Rank' the first column
columns = ['Rank'] + [col for col in df.columns if col != 'Rank']
df = df[columns]

# Replace NaN values with empty strings
df.fillna('', inplace=True)

# Convert the DataFrame to a list of dictionaries for easier rendering in the template
quiz_data = df.to_dict(orient='records')

@app.route('/')
def index():
    return render_template('index.html', quiz_data=quiz_data)

@app.route('/search', methods=['POST'])
def search():
    its_number = request.form.get('email')  # Get the ITS Number from the form
    print(f"Searching for ITS Number: {its_number}")  # Debug print
    its_number = its_number.strip()
    user_data = df[df['ITS Number'].astype(str).str.strip() == its_number].to_dict(orient='records')
    print(f"Filtered Data: {user_data}")  # Debug print
    return render_template('index.html', quiz_data=user_data)

if __name__ == '__main__':
    app.run(debug=True)
