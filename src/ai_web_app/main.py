from flask import Flask, request, jsonify
from functools import wraps
from .crew_integration import AICrewManager
from dotenv import load_dotenv
import os
import yaml
from werkzeug.exceptions import BadRequest, InternalServerError, Unauthorized
from .logging_config import setup_logger, logger as app_logger

# This should be stored securely, preferably in a database
TOKENS = {
    "secret-token-1": "user1",
    "secret-token-2": "user2",
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            app_logger.warning("Missing token")
            return jsonify({"error": "Missing token"}), 401
        if not token.startswith('Bearer '):
            app_logger.warning("Invalid token format")
            return jsonify({"error": "Invalid token format"}), 401
        token = token.split('Bearer ')[1]
        if token not in TOKENS:
            app_logger.warning("Invalid token")
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

def create_app(config_path='config/config.yaml'):
    load_dotenv('openai_key.env')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    app = Flask(__name__)
    app.config.update(config)

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
    @token_required
    def analyze_data():
        if not app.config['features'].get('enable_data_analysis', True):
            app_logger.warning("Data analysis feature is disabled")
            return jsonify(error="Feature Disabled", message="Data analysis feature is currently disabled"), 403
        
        try:
            data = request.json
            if not data:
                raise BadRequest("No data provided")
            
            app_logger.info(f"Analyzing data")
            result = ai_crew_manager.analyze_data(data)
            return jsonify(result)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during data analysis: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during data analysis")

    @app.route('/recommend', methods=['POST'])
    @token_required
    def get_recommendation():
        if not app.config['features'].get('enable_recommendations', True):
            app_logger.warning("Recommendations feature is disabled")
            return jsonify(error="Feature Disabled", message="Recommendations feature is currently disabled"), 403
        
        try:
            user_data = request.json
            if not user_data:
                raise BadRequest("No user data provided")
            
            app_logger.info(f"Getting recommendation")
            recommendation = ai_crew_manager.get_recommendation(user_data)
            return jsonify(recommendation)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during recommendation: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during recommendation generation")

    @app.route('/sentiment', methods=['POST'])
    @token_required
    def analyze_sentiment():
        if not app.config['features'].get('enable_sentiment_analysis', True):
            app_logger.warning("Sentiment analysis feature is disabled")
            return jsonify(error="Feature Disabled", message="Sentiment analysis feature is currently disabled"), 403
        
        try:
            text_data = request.json.get('text')
            if not text_data:
                raise BadRequest("No text provided for sentiment analysis")
            
            app_logger.info(f"Analyzing sentiment")
            sentiment = ai_crew_manager.analyze_sentiment(text_data)
            return jsonify(sentiment)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during sentiment analysis: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during sentiment analysis")
        
    @app.route('/generate-content', methods=['POST'])
    @token_required
    def generate_content():
        if not app.config['features'].get('enable_content_generation', True):
            app_logger.warning("Content generation feature is disabled")
            return jsonify(error="Feature Disabled", message="Content generation feature is currently disabled"), 403
        
        try:
            data = request.json
            if not data or 'topic' not in data or 'content_type' not in data:
                raise BadRequest("Topic and content type must be provided")
            
            app_logger.info(f"Generating content for topic: {data['topic']}")
            content = ai_crew_manager.generate_content(data['topic'], data['content_type'])
            return jsonify(content)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during content generation: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during content generation")

    @app.route('/comprehensive-analysis', methods=['POST'])
    @token_required
    def comprehensive_analysis():
        if not app.config['features'].get('enable_comprehensive_analysis', True):
            app_logger.warning("Comprehensive analysis feature is disabled")
            return jsonify(error="Feature Disabled", message="Comprehensive analysis feature is currently disabled"), 403
        
        try:
            data = request.json
            if not data:
                raise BadRequest("No data provided for analysis")
            
            app_logger.info("Performing comprehensive analysis")
            analysis = ai_crew_manager.comprehensive_analysis(data)
            return jsonify(analysis)
        except BadRequest as e:
            raise
        except Exception as e:
            app_logger.error(f"Error during comprehensive analysis: {str(e)}", exc_info=True)
            raise InternalServerError("An error occurred during comprehensive analysis")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['server']['host'],
        port=app.config['server']['port'],
        debug=app.config['app']['debug']
    )