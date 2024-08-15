from crewai import Agent, Task, Crew, Process

class AICrewManager:
    def __init__(self, api_key, model_name, max_tokens, temperature):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.analyst = Agent(
            role='Data Analyst',
            goal='Analyze data and provide insights',
            backstory='Expert in data analysis with years of experience',
            llm_config={
                'model': self.model_name,
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }
        )
        
        self.recommender = Agent(
            role='Recommendation Specialist',
            goal='Provide personalized recommendations',
            backstory='AI specialist in creating tailored suggestions',
            llm_config={
                'model': self.model_name,
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }
        )

        self.sentiment_analyzer = Agent(
            role='Sentiment Analyst',
            goal='Analyze sentiment in text data',
            backstory='Expert in natural language processing and sentiment analysis',
            llm_config={
                'model': self.model_name,
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }
        )

    def analyze_data(self, data):
        task = Task(
            description=f"Analyze the following data and provide insights: {data}",
            agent=self.analyst
        )
        crew = Crew(
            agents=[self.analyst],
            tasks=[task],
            process=Process.sequential
        )
        result = crew.kickoff()
        return result

    def get_recommendation(self, user_data):
        task = Task(
            description=f"Generate a personalized recommendation based on: {user_data}",
            agent=self.recommender
        )
        crew = Crew(
            agents=[self.recommender],
            tasks=[task],
            process=Process.sequential
        )
        result = crew.kickoff()
        return result

    def analyze_sentiment(self, text):
        task = Task(
            description=f"Analyze the sentiment of the following text: {text}",
            agent=self.sentiment_analyzer
        )
        crew = Crew(
            agents=[self.sentiment_analyzer],
            tasks=[task],
            process=Process.sequential
        )
        result = crew.kickoff()
        return result