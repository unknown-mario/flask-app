from flask import Flask, render_template, request

app = Flask(__name__)

# Symptom database
symptoms_data = {
    "headache": {"cause": "Stress or dehydration", "remedy": "Drink water and rest"},
    "fever": {"cause": "Infection", "remedy": "Take paracetamol, rest, and stay hydrated"},
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    symptom = request.form['symptom'].lower()
    data = symptoms_data.get(symptom, {"cause": "Unknown", "remedy": "Consult a doctor if severe"})
    return render_template('result.html', symptom=symptom, cause=data['cause'], remedy=data['remedy'])

if __name__ == '__main__':
    app.run(debug=True)
