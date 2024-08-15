# ... (previous code remains the same)

@app.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    if not config['features'].get('enable_sentiment_analysis', False):
        logger.warning("Sentiment analysis feature is disabled")
        return jsonify({"error": "Feature Disabled", "message": "Sentiment analysis feature is currently disabled"}), 403
    
    try:
        text_data = request.json.get('text')
        if not text_data:
            raise ValueError("No text provided for sentiment analysis")
        
        logger.info(f"Analyzing sentiment for text: {text_data[:50]}...")  # Log only the first 50 characters
        sentiment = ai_crew_manager.analyze_sentiment(text_data)
        return jsonify(sentiment)
    except ValueError as e:
        logger.error(f"Invalid data for sentiment analysis: {str(e)}")
        return jsonify({"error": "Invalid Data", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {str(e)}")
        return jsonify({"error": "Sentiment Analysis Error", "message": "An error occurred during sentiment analysis"}), 500

# ... (rest of the code remains the same)