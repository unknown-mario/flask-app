from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form['symptoms']
    diagnosis = "Possible diagnosis based on symptoms: " + symptoms
    return render_template('result.html', diagnosis=diagnosis)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
