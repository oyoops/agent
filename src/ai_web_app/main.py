from flask import Flask, request, jsonify
from .crew_integration import AICrewManager
from .logging_config import logger
from dotenv import load_dotenv
import os
import yaml

# Load environment variables and configuration
load_dotenv('openai_key.env')
with open('config/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

app = Flask(__name__)
app.config.update(config['app'])

ai_crew_manager = AICrewManager(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name=config['ai']['model_name'],
    max_tokens=config['ai']['max_tokens'],
    temperature=config['ai']['temperature']
)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"An error occurred: {error}")
    return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@app.route('/')
def home():
    logger.info("Home route accessed")
    return f"Welcome to {config['app']['name']}!"

@app.route('/analyze', methods=['POST'])
def analyze_data():
    if not config['features']['enable_data_analysis']:
        logger.warning("Data analysis feature is disabled")
        return jsonify({"error": "Feature Disabled", "message": "Data analysis feature is currently disabled"}), 403
    
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")
        
        logger.info(f"Analyzing data: {data}")
        result = ai_crew_manager.analyze_data(data)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"Invalid data for analysis: {str(e)}")
        return jsonify({"error": "Invalid Data", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error during data analysis: {str(e)}")
        return jsonify({"error": "Analysis Error", "message": "An error occurred during data analysis"}), 500

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    if not config['features']['enable_recommendations']:
        logger.warning("Recommendations feature is disabled")
        return jsonify({"error": "Feature Disabled", "message": "Recommendations feature is currently disabled"}), 403
    
    try:
        user_data = request.json
        if not user_data:
            raise ValueError("No user data provided")
        
        logger.info(f"Getting recommendation for user data: {user_data}")
        recommendation = ai_crew_manager.get_recommendation(user_data)
        return jsonify(recommendation)
    except ValueError as e:
        logger.error(f"Invalid user data for recommendation: {str(e)}")
        return jsonify({"error": "Invalid Data", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error during recommendation: {str(e)}")
        return jsonify({"error": "Recommendation Error", "message": "An error occurred during recommendation generation"}), 500

if __name__ == '__main__':
    logger.info(f"Starting {config['app']['name']}")
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['app']['debug']
    )