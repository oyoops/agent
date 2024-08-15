from flask import Flask, request, jsonify
from .crew_integration import AICrewManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('openai_key.env')

app = Flask(__name__)
ai_crew_manager = AICrewManager(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def home():
    return "Welcome to AI Web App!"

@app.route('/analyze', methods=['POST'])
def analyze_data():
    data = request.json
    result = ai_crew_manager.analyze_data(data)
    return jsonify(result)

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    user_data = request.json
    recommendation = ai_crew_manager.get_recommendation(user_data)
    return jsonify(recommendation)

if __name__ == '__main__':
    app.run(debug=True)