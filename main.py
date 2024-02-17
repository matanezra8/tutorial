from flask import Flask, render_template, request, jsonify
import pandas as pd
from flask_caching import Cache

app = Flask(__name__)

# Configure the Flask app to use Flask-Caching
app.config['CACHE_TYPE'] = 'simple'  # You can choose a different caching type
cache = Cache(app)

# Assume you have a DataFrame with columns represented as a dictionary of lists
data = {
    'Column1': ['apple','apple', 'banana', 'cherry', 'date', 'grape'],
    'Column2': ['apple','red', 'yellow', 'green', 'brown', 'purple'],
    'Column3': ['apple','car', 'bus', 'bike', 'train', 'plane']
}

df = pd.DataFrame(data)

# Convert DataFrame columns to a dictionary of lists
columns_dict = df.to_dict(orient='list')
unique_values_dict = {column: df[column].unique().tolist() for column in df.columns}
cache.set('my_values', unique_values_dict)



@app.route('/')
def index():
    return render_template('index.html', columns_dict=columns_dict)

@app.route('/suggest', methods=['GET'])
def suggest():
    column_name = request.args.get('column', '')
    search_term = request.args.get('term', '')
    unique_values_dict = cache.get('my_values')
    print(unique_values_dict)
    if column_name in columns_dict:
        column_values = unique_values_dict[column_name]
        suggestions = [value for value in column_values if search_term.lower() in value.lower()]
        return jsonify(suggestions)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
