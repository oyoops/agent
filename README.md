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

## Local Development

To run the application locally:

```
python src/ai_web_app/main.py
```

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

1. Create new agent definitions in `src/ai_web_app/crew_integration.py`
2. Add new methods to the `AICrewManager` class for specific AI tasks
3. Create new routes in `src/ai_web_app/main.py` to expose the AI functionality

## Monitoring and Scaling

- Use AWS CloudWatch to monitor application performance
- Adjust auto-scaling settings in the Elastic Beanstalk console or by modifying the `config/aws-config.yaml` file

## Running Tests

To run tests:

```
pytest tests/
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.