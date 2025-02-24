from flask import Flask, request, render_template

app = Flask(__name__)

# Symptom Database: Causes & Remedies
symptom_data = {
    "fever": {
        "cause": "Fever is usually caused by infections, including the flu or cold.",
        "remedies": "Drink plenty of fluids, rest, take paracetamol if necessary.",
        "doctor": "See a doctor if fever lasts more than 3 days or is very high."
    },
    "cough": {
        "cause": "Coughing is often due to viral infections, allergies, or irritation.",
        "remedies": "Drink warm tea with honey, inhale steam, avoid cold drinks.",
        "doctor": "Visit a doctor if cough persists for more than 2 weeks."
    },
    "headache": {
        "cause": "Can be caused by stress, dehydration, or migraines.",
        "remedies": "Drink water, rest in a dark room, try a cold compress.",
        "doctor": "Consult a doctor if headaches are severe or frequent."
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form['symptoms'].lower().split(", ")  # Convert input into a list
    report = {}

    for symptom in symptoms:
        if symptom in symptom_data:
            report[symptom] = symptom_data[symptom]
        else:
            report[symptom] = {
                "cause": "Not found in our database.",
                "remedies": "Try resting and drinking fluids.",
                "doctor": "Consult a doctor if symptoms persist."
            }

    return render_template('result.html', report=report)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
