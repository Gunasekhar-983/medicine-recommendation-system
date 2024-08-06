from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the medicine dataframe from pickle
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)

# Load the similarity vector data from pickle
similarity = pickle.load(open('medicine_similar.pkl', 'rb'))

def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        drug_name = medicines.iloc[i[0]].Drug_Name
        # Construct a basic URL for PharmEasy
        drug_url = f"https://pharmeasy.in/search/all?name={'%20'.join(drug_name.split())}"
        recommended_medicines.append((drug_name, drug_url))
    return recommended_medicines

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_medicine_name = None
    if request.method == 'POST':
        selected_medicine_name = request.form.get('medicine')
        recommendations = recommend(selected_medicine_name)

    medicines_list = medicines['Drug_Name'].values
    return render_template('index.html', medicines_list=medicines_list, recommendations=recommendations, selected_medicine_name=selected_medicine_name)

if __name__ == '__main__':
    app.run(debug=True)
