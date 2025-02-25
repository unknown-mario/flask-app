from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Sample database of symptoms and conditions
conditions_data = {
    'condition': [
        'Common Cold', 
        'Influenza (Flu)', 
        'COVID-19',
        'Allergic Rhinitis', 
        'Gastroenteritis', 
        'Migraine',
        'Tension Headache',
        'Urinary Tract Infection',
        'Asthma',
        'Bronchitis'
    ],
    'symptoms': [
        'runny nose, sneezing, sore throat, cough, congestion, slight body aches, mild headache',
        'fever, chills, body aches, headache, fatigue, cough, sore throat, congestion',
        'fever, cough, shortness of breath, fatigue, body aches, loss of taste or smell, sore throat',
        'sneezing, itchy nose, runny nose, congestion, itchy eyes, watery eyes',
        'diarrhea, nausea, vomiting, abdominal cramps, fever, headache',
        'throbbing headache, sensitivity to light, nausea, vomiting, vision changes',
        'dull headache, pressure around forehead, tenderness in scalp, neck or shoulder pain',
        'burning urination, frequent urination, cloudy urine, strong odor, pelvic pain',
        'shortness of breath, wheezing, chest tightness, coughing, especially at night',
        'persistent cough with mucus, shortness of breath, wheezing, chest discomfort, fatigue'
    ],
    'recommendations': [
        'Rest, stay hydrated, use over-the-counter cold medications if needed. See a doctor if symptoms worsen after a week.',
        'Rest, stay hydrated, take fever reducers. Consult a doctor especially if you have risk factors.',
        'Isolate, rest, stay hydrated. Contact a healthcare provider for testing and guidance, especially if experiencing severe symptoms.',
        'Avoid allergens, try over-the-counter antihistamines, or consult with a healthcare provider for prescription medications.',
        'Stay hydrated, eat bland foods, get rest. Seek medical attention if symptoms are severe or persist beyond 3 days.',
        'Rest in a dark, quiet room. Consider over-the-counter pain relievers. Consult a doctor for recurring migraines.',
        'Rest, use over-the-counter pain relievers, manage stress. See a doctor if headaches are frequent or severe.',
        'Drink plenty of water, urinate frequently, use over-the-counter pain relievers. See a doctor for antibiotics.',
        'Use prescribed inhalers, avoid triggers, follow your asthma action plan. Seek emergency care for severe attacks.',
        'Rest, stay hydrated, use over-the-counter pain relievers. See a doctor if symptoms persist or worsen.'
    ],
    'severity': [
        'Mild',
        'Moderate',
        'Moderate to Severe',
        'Mild',
        'Moderate',
        'Moderate',
        'Mild',
        'Moderate',
        'Moderate to Severe',
        'Moderate'
    ]
}

# Create a dataframe
conditions_df = pd.DataFrame(conditions_data)

# Vectorizer for symptom matching
vectorizer = TfidfVectorizer(stop_words='english')
symptom_vectors = vectorizer.fit_transform(conditions_df['symptoms'])

def get_condition_matches(user_symptoms, top_n=3):
    """Match user symptoms to conditions and return top matches"""
    # Vectorize user input
    user_vector = vectorizer.transform([user_symptoms])
    
    # Calculate similarity
    similarity_scores = cosine_similarity(user_vector, symptom_vectors).flatten()
    
    # Get top matches
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    
    results = []
    for i in top_indices:
        if similarity_scores[i] > 0.1:  # Only include if there's some meaningful similarity
            results.append({
                'condition': conditions_df.iloc[i]['condition'],
                'similarity': float(similarity_scores[i]),
                'recommendation': conditions_df.iloc[i]['recommendations'],
                'severity': conditions_df.iloc[i]['severity']
            })
    
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_symptoms = data.get('symptoms', '')
    
    if not user_symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    matches = get_condition_matches(user_symptoms)
    
    report = {
        'symptoms_entered': user_symptoms,
        'possible_conditions': matches,
        'disclaimer': 'This is not a medical diagnosis. Please consult with a healthcare professional for proper evaluation and treatment.'
    }
    
    return jsonify(report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
