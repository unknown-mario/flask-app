from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Expanded database with more comprehensive information
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
        'Bronchitis',
        'Lower Back Pain',
        'Anxiety',
        'Insomnia'
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
        'persistent cough with mucus, shortness of breath, wheezing, chest discomfort, fatigue',
        'lower back pain, muscle ache, stiffness, limited range of motion, pain that worsens with bending',
        'excessive worry, restlessness, fatigue, difficulty concentrating, irritability, muscle tension',
        'difficulty falling asleep, staying asleep, waking up too early, daytime tiredness, irritability'
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
        'Rest, stay hydrated, use over-the-counter pain relievers. See a doctor if symptoms persist or worsen.',
        'Apply ice for the first 48-72 hours, then heat. Gentle stretching, over-the-counter pain relievers. Maintain good posture.',
        'Practice deep breathing, progressive muscle relaxation, regular exercise, and good sleep hygiene. Limit caffeine and alcohol.',
        'Establish a regular sleep schedule, create a comfortable sleep environment, avoid screens before bed, limit caffeine and alcohol.'
    ],
    'home_remedies': [
        'Garlic tea, honey with warm water, salt water gargle for sore throat, steam inhalation with eucalyptus oil',
        'Ginger tea with honey and lemon, chicken soup, rest in a humid environment, stay well hydrated',
        'Warm salt water gargle, steam inhalation, herbal tea with honey, separate utensils and living space',
        'Local honey (for pollen allergies), saline nasal rinse, steam inhalation, drinking nettle leaf tea',
        'BRAT diet (bananas, rice, applesauce, toast), ginger tea, clear broth, activated charcoal for diarrhea',
        'Peppermint oil on temples, ice pack on forehead, drinking plenty of water, 2 cups of strong coffee for caffeine',
        'Peppermint or lavender essential oil on temples, warm shower or bath, herbal tea, neck stretches',
        'Unsweetened cranberry juice, increasing water intake, avoiding irritants like coffee and alcohol',
        'Steam inhalation, staying hydrated, breathing exercises, avoiding triggers like dust and pollen',
        'Honey with warm water, steam inhalation, salt water gargle, staying hydrated',
        'Turmeric milk, gentle yoga stretches, heat/ice therapy, maintaining good posture, firm mattress support',
        'Chamomile tea, lavender essential oil, meditation, deep breathing exercises, limiting screen time',
        'Valerian root tea, warm milk with honey, lavender essential oil diffuser, limiting screen time before bed'
    ],
    'exercises_or_yoga': [
        'Gentle walking, deep breathing exercises',
        'Rest is recommended until fever subsides, then gentle walking if feeling better',
        'Deep breathing exercises when recovered, gradual return to activity after isolation period',
        'Pranayama breathing exercises, gentle yoga to reduce stress',
        'Rest during active symptoms, gentle walking when recovering',
        'Neck stretches, shoulder rolls, gentle yoga (avoid inversions during migraine)',
        'Neck stretches, shoulder rolls, gentle head rotations, stress-relief yoga',
        'Kegel exercises, gentle walking, pelvic floor stretches',
        'Breathing exercises, gentle yoga focused on breath control (pranayama)',
        'Breathing exercises, gentle chest expansion stretches',
        'Cat-cow pose, child's pose, sphinx pose, bridge pose, gentle twists, walking',
        'Sun salutation, alternate nostril breathing, corpse pose, child's pose, forward fold',
        'Legs-up-the-wall pose, corpse pose, seated forward bend, butterfly pose, alternate nostril breathing'
    ],
    'when_to_see_doctor': [
        'If fever exceeds 101.3°F (38.5°C), symptoms last longer than 10 days, or breathing becomes difficult',
        'If fever is high (above 103°F/39.4°C), breathing becomes difficult, or you're in a high-risk group',
        'If you have severe shortness of breath, persistent chest pain, confusion, bluish lips, or high fever',
        'If over-the-counter medications don't help, symptoms are severe, or sinusitis develops',
        'If symptoms last more than 2 days, severe abdominal pain, high fever, bloody stools, or signs of dehydration',
        'If it's your first severe headache, headache is sudden and severe, accompanied by fever, stiff neck, confusion, seizure, double vision, weakness, or numbness',
        'If headaches are frequent, severe, don't respond to over-the-counter medications, or interfere with daily activities',
        'If symptoms don't improve within 2 days, fever, back pain, blood in urine, or if you're pregnant',
        'If you have severe shortness of breath, symptoms don't improve with inhaler, lips/face turns blue, or extreme difficulty breathing',
        'If symptoms last more than 3 weeks, produce blood when coughing, high fever, or difficulty breathing',
        'If pain radiates down legs, causes numbness/tingling, is accompanied by bowel/bladder issues, follows an injury, or lasts longer than 2 weeks',
        'If symptoms interfere with daily functioning, you have thoughts of harming yourself, or anxiety persists for weeks',
        'If insomnia persists for more than a month, interferes with daily life, or comes with breathing difficulties or chest pain while sleeping'
    ],
    'specialist_type': [
        'Primary Care Physician or Family Doctor',
        'Primary Care Physician or Infectious Disease Specialist',
        'Primary Care Physician or Infectious Disease Specialist',
        'Allergist or Ear, Nose, and Throat (ENT) Specialist',
        'Gastroenterologist or Primary Care Physician',
        'Neurologist or Headache Specialist',
        'Neurologist or Primary Care Physician',
        'Urologist or Primary Care Physician',
        'Pulmonologist or Allergist',
        'Pulmonologist or Primary Care Physician',
        'Orthopedist, Physical Therapist, or Spine Specialist',
        'Psychiatrist, Psychologist, or Mental Health Counselor',
        'Sleep Specialist or Psychiatrist'
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
        'Moderate',
        'Mild to Moderate',
        'Mild to Severe',
        'Mild to Moderate'
    ],
    'age_specific_info': [
        'Children may have more runny nose than adults. Elderly may develop complications like pneumonia more easily.',
        'Children may develop higher fevers than adults. High-risk groups include the elderly, pregnant women, and those with chronic conditions.',
        'Elderly and those with pre-existing conditions (diabetes, heart/lung disease) are at higher risk for severe symptoms. Children usually have milder symptoms.',
        'May start in childhood and improve with age. Can worsen during pregnancy. More common in people with family history of allergies.',
        'More dangerous for young children and elderly due to risk of dehydration. Monitor fluid intake carefully in these groups.',
        'Often begins in puberty to early adulthood. Can be triggered by hormonal changes during menstruation, pregnancy, or menopause.',
        'Can affect all ages but more common in adults. Often triggered by stress and poor posture.',
        'More common in women. Pregnant women should seek immediate treatment. Men with symptoms should see a doctor promptly as this may indicate prostate issues.',
        'Often begins in childhood. Can be more dangerous for elderly. Pregnancy may improve or worsen symptoms.',
        'More serious in young children, elderly, smokers, and those with weakened immune systems.',
        'More common with age (30-50 years). Pregnancy can worsen symptoms. Children rarely have true low back pain (may indicate serious condition).',
        'Can begin at any age, even childhood. Adolescents often experience symptoms during school transitions. Pregnancy and postpartum can trigger or worsen anxiety.',
        'More common in elderly and during pregnancy. Children with insomnia should be evaluated for underlying conditions.'
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
                'home_remedies': conditions_df.iloc[i]['home_remedies'],
                'exercises_yoga': conditions_df.iloc[i]['exercises_or_yoga'],
                'when_to_see_doctor': conditions_df.iloc[i]['when_to_see_doctor'],
                'specialist_type': conditions_df.iloc[i]['specialist_type'],
                'severity': conditions_df.iloc[i]['severity'],
                'age_specific_info': conditions_df.iloc[i]['age_specific_info']
            })
    
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_symptoms = data.get('symptoms', '')
    family_member = data.get('familyMember', 'self')
    age_group = data.get('ageGroup', 'adult')
    
    if not user_symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    matches = get_condition_matches(user_symptoms)
    
    report = {
        'symptoms_entered': user_symptoms,
        'family_member': family_member,
        'age_group': age_group,
        'possible_conditions': matches,
        'disclaimer': 'This is not a medical diagnosis. Please consult with a healthcare professional for proper evaluation and treatment.'
    }
    
    return jsonify(report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
