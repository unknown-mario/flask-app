from flask import Flask, render_template, request, jsonify
import time  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message")
    time.sleep(1)  # Simulating AI response delay
    response = f"AI Doctor: Based on your symptoms, you might need rest and hydration!"
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
