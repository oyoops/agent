from flask import Flask, request, jsonify
from .crew_integration import AICrewManager
from dotenv import load_dotenv
import os
import yaml
from werkzeug.exceptions import BadRequest, InternalServerError
from .logging_config import setup_logger, logger as app_logger

def create_app(config_path='config/config.yaml'):
    load_dotenv('openai_key.env')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    app = Flask(__name__)
    app.config.update(config)

    # Setup logger
    global app_logger
    app_logger = setup_logger(config)

    ai_crew_manager = AICrewManager(
        api_key=os.getenv('OPENAI_API_KEY'),
        model_name=app.config['ai']['model_name'],
        max_tokens=app.config['ai']['max_tokens'],
        temperature=app.config['ai']['temperature']
    )

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        app_logger.warning(f"Bad request: {str(e)}")
        return jsonify(error="Bad Request", message=str(e)), 400

    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(e):
        app_logger.error(f"Internal server error: {str(e)}")
        return jsonify(error="Internal Server Error", message="An unexpected error occurred"), 500

    @app.route('/')
    def home():
        app_logger.info("Home route accessed")
        return f"Welcome to {app.config['app']['name']}!"

    @app.route('/analyze', methods=['POST'])
    def analyze_data():
        if not app.config['features'].get('enable_data_analysis', True):
            app_logger.warning("Data analysis feature is disabled")
            return jsonify(error="Feature Disabled", message="Data analysis feature is currently disabled"), 403
        
        try:
            data = request.json
            if not data:
                raise BadRequest("No data provided")
            
            app_logger.info(f"Analyzing data: {data}")
            result = ai_crew_manager.analyze_data(data)
            return jsonify(result)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during data analysis: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during data analysis")

    @app.route('/recommend', methods=['POST'])
    def get_recommendation():
        if not app.config['features'].get('enable_recommendations', True):
            app_logger.warning("Recommendations feature is disabled")
            return jsonify(error="Feature Disabled", message="Recommendations feature is currently disabled"), 403
        
        try:
            user_data = request.json
            if not user_data:
                raise BadRequest("No user data provided")
            
            app_logger.info(f"Getting recommendation for user data: {user_data}")
            recommendation = ai_crew_manager.get_recommendation(user_data)
            return jsonify(recommendation)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during recommendation: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during recommendation generation")

    @app.route('/sentiment', methods=['POST'])
    def analyze_sentiment():
        if not app.config['features'].get('enable_sentiment_analysis', True):
            app_logger.warning("Sentiment analysis feature is disabled")
            return jsonify(error="Feature Disabled", message="Sentiment analysis feature is currently disabled"), 403
        
        try:
            text_data = request.json.get('text')
            if not text_data:
                raise BadRequest("No text provided for sentiment analysis")
            
            app_logger.info(f"Analyzing sentiment for text: {text_data[:50]}...")
            sentiment = ai_crew_manager.analyze_sentiment(text_data)
            return jsonify(sentiment)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during sentiment analysis: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during sentiment analysis")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['server']['host'],
        port=app.config['server']['port'],
        debug=app.config['app']['debug']
    )