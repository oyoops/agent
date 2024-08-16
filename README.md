# 🤖 AI Web App

## 🌟 Overview

AI Web App is a Flask-based application that leverages the power of CrewAI to provide intelligent data analysis, recommendations, and sentiment analysis. This project demonstrates the integration of AI capabilities into a web application, making it easy to deploy and scale AI-powered services.

## 🚀 Features

- 📊 Data Analysis: Analyze complex datasets and provide insightful results.
- 🎯 Personalized Recommendations: Generate tailored recommendations based on user data.
- 😃 Sentiment Analysis: Determine the sentiment of text inputs.
- 🔧 Configurable AI Agents: Easily add or modify AI agents to extend functionality.
- 🔒 Feature Toggles: Enable or disable specific AI features as needed.

## 🛠️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-web-app.git
   cd ai-web-app
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install poetry
   poetry install
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file

## 🖥️ Usage

1. Start the application:
   ```
   poetry run python src/ai_web_app/main.py
   ```

2. Access the API endpoints:
   - Home: `GET /`
   - Analyze Data: `POST /analyze`
   - Get Recommendation: `POST /recommend`
   - Analyze Sentiment: `POST /sentiment`

## 🧪 Running Tests

Run the test suite using pytest:
```
poetry run pytest
```

## 📚 API Documentation

### Analyze Data
- Endpoint: `POST /analyze`
- Request Body: `{ "data": "Your data here" }`
- Response: JSON object with analysis results

### Get Recommendation
- Endpoint: `POST /recommend`
- Request Body: `{ "user": "User data here" }`
- Response: JSON object with personalized recommendations

### Analyze Sentiment
- Endpoint: `POST /sentiment`
- Request Body: `{ "text": "Text to analyze" }`
- Response: JSON object with sentiment analysis results

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [CrewAI](https://github.com/joaomdmoura/crewAI) for providing the AI framework
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [OpenAI](https://openai.com/) for the language model capabilities