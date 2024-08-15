# AI Web App

This is an AI-powered web application built with Python, Flask, and Crew.ai, deployed on AWS Elastic Beanstalk.

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   poetry install
   ```
3. Activate the virtual environment:
   ```
   poetry shell
   ```
4. Copy `openai_key.env.example` to `openai_key.env` and add your OpenAI API key
5. Review and update `config/config.yaml` as needed

## Local Development

To run the application locally:

```
python src/ai_web_app/main.py
```

## Configuration

The application uses a `config.yaml` file located in the `config/` directory. Review and update this file to change application settings, AI parameters, and feature flags.

## Environment Variables

Sensitive information is stored in environment variables. Create a `openai_key.env` file based on the `openai_key.env.example` template and add your API keys and other sensitive data.

## Logging

Logging is configured in `src/ai_web_app/logging_config.py`. Adjust the logging level and format in `config.yaml` as needed.

## AWS Deployment

1. Install the AWS CLI and configure it with your credentials.
2. Install the Elastic Beanstalk CLI:
   ```
   pip install awsebcli
   ```
3. Initialize Elastic Beanstalk in your project:
   ```
   eb init -p python-3.8 ai-web-app --region us-west-2
   ```
4. Create an Elastic Beanstalk environment:
   ```
   eb create ai-web-app-env
   ```
5. Deploy your application:
   ```
   eb deploy
   ```

## Extending AI Features

To add new AI features:

1. Update `config.yaml` with any new AI-related settings
2. Modify `src/ai_web_app/crew_integration.py` to add new agent definitions or tasks
3. Update `src/ai_web_app/main.py` to expose new AI functionality via API endpoints

## Running Tests

To run tests:

```
pytest tests/
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.