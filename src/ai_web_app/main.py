from flask import Flask, request, jsonify
from .crew_integration import AICrewManager
from .logging_config import logger
from dotenv import load_dotenv
import os
import yaml

# Load environment variables
load_dotenv('openai_key.env')

# Load configuration
with open('config/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

app = Flask(__name__)
app.config.update(config['app'])

# Use configuration in AICrewManager initialization
ai_crew_manager = AICrewManager(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name=config['ai']['model_name'],
    max_tokens=config['ai']['max_tokens'],
    temperature=config['ai']['temperature']
)

@app.route('/')
def home():
    logger.info("Home route accessed")
    return f"Welcome to {config['app']['name']}!"

@app.route('/analyze', methods=['POST'])
def analyze_data():
    if not config['features']['enable_data_analysis']:
        logger.warning("Data analysis feature is disabled")
        return jsonify({"error": "Data analysis feature is disabled"}), 403
    data = request.json
    logger.info(f"Analyzing data: {data}")
    result = ai_crew_manager.analyze_data(data)
    return jsonify(result)

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    if not config['features']['enable_recommendations']:
        logger.warning("Recommendations feature is disabled")
        return jsonify({"error": "Recommendations feature is disabled"}), 403
    user_data = request.json
    logger.info(f"Getting recommendation for user data: {user_data}")
    recommendation = ai_crew_manager.get_recommendation(user_data)
    return jsonify(recommendation)

if __name__ == '__main__':
    logger.info(f"Starting {config['app']['name']}")
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['app']['debug']
    )