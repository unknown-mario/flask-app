from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Sample database of symptoms and conditions
# In a real application, you would want a much more comprehensive database
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

# Create a simple HTML template for the app
@app.route('/templates/index.html')
def get_index_template():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Symptom Analyzer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
            }
            .input-area {
                margin-bottom: 20px;
            }
            textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                height: 100px;
                font-size: 16px;
            }
            button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
            }
            .result {
                margin-top: 20px;
                border-top: 1px solid #eee;
                padding-top: 20px;
            }
            .condition {
                margin-bottom: 15px;
                padding: 15px;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            .condition h3 {
                margin-top: 0;
                color: #2c3e50;
            }
            .disclaimer {
                font-style: italic;
                color: #e74c3c;
                margin-top: 20px;
                text-align: center;
            }
            .loading {
                text-align: center;
                display: none;
            }
            .severity-mild {
                border-left: 5px solid #2ecc71;
            }
            .severity-moderate {
                border-left: 5px solid #f39c12;
            }
            .severity-severe {
                border-left: 5px solid #e74c3c;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Symptom Analyzer</h1>
            <div class="input-area">
                <p>Describe your symptoms in detail:</p>
                <textarea id="symptoms" placeholder="Example: fever, cough, headache, fatigue..."></textarea>
                <button onclick="analyzeSymptoms()">Analyze Symptoms</button>
            </div>
            <div class="loading" id="loading">
                <p>Analyzing symptoms...</p>
            </div>
            <div class="result" id="result" style="display:none;">
                <h2>Analysis Report</h2>
                <div id="report-content"></div>
                <p class="disclaimer">This is not a medical diagnosis. Please consult with a healthcare professional for proper evaluation and treatment.</p>
            </div>
        </div>

        <script>
            function analyzeSymptoms() {
                const symptoms = document.getElementById('symptoms').value;
                if (!symptoms) {
                    alert('Please enter your symptoms');
                    return;
                }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').style.display = 'none';
                
                fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ symptoms: symptoms }),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('result').style.display = 'block';
                    
                    let html = `<p><strong>Symptoms analyzed:</strong> ${data.symptoms_entered}</p>`;
                    
                    if (data.possible_conditions.length === 0) {
                        html += '<p>No conditions matched your symptoms. Please provide more details or consult a healthcare professional.</p>';
                    } else {
                        html += '<h3>Possible Conditions:</h3>';
                        
                        data.possible_conditions.forEach(condition => {
                            const severityClass = condition.severity.toLowerCase().includes('severe') 
                                ? 'severity-severe' 
                                : (condition.severity.toLowerCase().includes('moderate') 
                                    ? 'severity-moderate' 
                                    : 'severity-mild');
                            
                            html += `
                                <div class="condition ${severityClass}">
                                    <h3>${condition.condition}</h3>
                                    <p><strong>Match confidence:</strong> ${Math.round(condition.similarity * 100)}%</p>
                                    <p><strong>Severity:</strong> ${condition.severity}</p>
                                    <p><strong>Recommendation:</strong> ${condition.recommendation}</p>
                                </div>
                            `;
                        });
                    }
                    
                    document.getElementById('report-content').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    alert('Error analyzing symptoms. Please try again.');
                    console.error('Error:', error);
                });
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
