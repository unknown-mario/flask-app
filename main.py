from flask import Flask, render_template, request

app = Flask(__name__)

# Symptom database
symptom_data = {
    "fever": {
        "cause": "Fever is usually caused by infections, including flu, cold, or viral infections.",
        "remedies": "Drink plenty of fluids, rest, take paracetamol if necessary.",
        "doctor": "See a doctor if fever lasts more than 3 days or is above 102°F."
    },
    "cough": {
        "cause": "Coughing is often due to viral infections, allergies, or throat irritation.",
        "remedies": "Drink warm tea with honey, inhale steam, avoid cold drinks.",
        "doctor": "Visit a doctor if cough persists for more than 2 weeks."
    },
    "headache": {
        "cause": "Common causes include stress, dehydration, or migraines.",
        "remedies": "Drink water, rest in a dark room, try a cold compress.",
        "doctor": "Consult a doctor if headaches are severe or frequent."
    },
    "cold": {
        "cause": "Caused by viral infections affecting the respiratory tract.",
        "remedies": "Drink warm fluids, take steam inhalation, and rest well.",
        "doctor": "See a doctor if symptoms last more than 10 days."
    },
    "sore throat": {
        "cause": "Often caused by viral infections, bacteria, or allergies.",
        "remedies": "Gargle with warm salt water, drink herbal tea, avoid cold drinks.",
        "doctor": "Consult a doctor if you have difficulty swallowing or a high fever."
    },
    "stomach pain": {
        "cause": "Causes include indigestion, acidity, or infections.",
        "remedies": "Drink warm water, eat light meals, take probiotics.",
        "doctor": "See a doctor if pain is severe or accompanied by vomiting."
    },
    "diarrhea": {
        "cause": "Commonly due to food poisoning, infections, or stress.",
        "remedies": "Stay hydrated, take oral rehydration salts (ORS), avoid spicy food.",
        "doctor": "Consult a doctor if diarrhea lasts more than 3 days."
    },
    "constipation": {
        "cause": "Caused by lack of fiber, dehydration, or inactivity.",
        "remedies": "Eat fiber-rich foods, drink water, exercise regularly.",
        "doctor": "See a doctor if constipation lasts more than a week."
    },
    "vomiting": {
        "cause": "Often due to food poisoning, infections, or motion sickness.",
        "remedies": "Drink ginger tea, sip clear fluids, avoid solid foods temporarily.",
        "doctor": "Seek medical help if vomiting is persistent or has blood."
    },
    "fatigue": {
        "cause": "Can be caused by stress, poor sleep, or anemia.",
        "remedies": "Get enough rest, eat a balanced diet, stay hydrated.",
        "doctor": "Consult a doctor if fatigue is unexplained or long-lasting."
    },
    "body pain": {
        "cause": "Commonly due to flu, physical exertion, or vitamin deficiency.",
        "remedies": "Take a warm bath, stay hydrated, do light stretching.",
        "doctor": "Visit a doctor if pain persists for more than a week."
    },
    "back pain": {
        "cause": "Caused by poor posture, muscle strain, or injury.",
        "remedies": "Apply a hot/cold compress, maintain good posture, do stretching exercises.",
        "doctor": "See a doctor if pain is severe or lasts more than a month."
    },
    "joint pain": {
        "cause": "Could be due to arthritis, inflammation, or overuse.",
        "remedies": "Apply ice packs, take turmeric milk, do light exercises.",
        "doctor": "Consult a doctor if joint pain is persistent or worsens."
    },
    "shortness of breath": {
        "cause": "Can be due to asthma, anxiety, or lung infections.",
        "remedies": "Practice deep breathing, sit upright, use a humidifier.",
        "doctor": "Seek emergency care if breathing difficulty is severe."
    },
    "dizziness": {
        "cause": "Common causes include dehydration, low blood sugar, or anemia.",
        "remedies": "Drink water, sit down and rest, eat something light.",
        "doctor": "See a doctor if dizziness is frequent or accompanied by fainting."
    },
    "chest pain": {
        "cause": "May indicate heart issues, acid reflux, or muscle strain.",
        "remedies": "Drink warm water, rest, avoid heavy meals.",
        "doctor": "Seek emergency help if pain is severe or radiates to the arm."
    },
    "skin rash": {
        "cause": "Could be due to allergies, infections, or skin conditions.",
        "remedies": "Apply aloe vera gel, avoid scratching, use mild soap.",
        "doctor": "Consult a doctor if rash spreads or causes discomfort."
    },
    "itching": {
        "cause": "Commonly caused by allergies, dry skin, or infections.",
        "remedies": "Moisturize skin, use calamine lotion, avoid harsh soaps.",
        "doctor": "See a doctor if itching is persistent or severe."
    },
    "eye redness": {
        "cause": "Can be due to infections, allergies, or strain.",
        "remedies": "Use cold compress, avoid rubbing eyes, rest properly.",
        "doctor": "Visit an eye doctor if redness persists or vision is affected."
    },
    "nausea": {
        "cause": "Often due to food poisoning, pregnancy, or motion sickness.",
        "remedies": "Drink ginger tea, eat light meals, avoid strong odors.",
        "doctor": "Seek medical advice if nausea is persistent or severe."
    },
    "insomnia": {
        "cause": "Caused by stress, anxiety, or irregular sleep patterns.",
        "remedies": "Maintain a bedtime routine, avoid caffeine, meditate.",
        "doctor": "See a doctor if sleep problems continue for weeks."
    },
    "loss of appetite": {
        "cause": "May be due to infections, stress, or digestive problems.",
        "remedies": "Eat small meals, drink herbal tea, stay hydrated.",
        "doctor": "Consult a doctor if appetite loss persists for a long time."
    },
    "frequent urination": {
        "cause": "Can be a sign of diabetes, infection, or high fluid intake.",
        "remedies": "Limit caffeine, stay hydrated, avoid sugary drinks.",
        "doctor": "See a doctor if urination is painful or very frequent."
    }
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
