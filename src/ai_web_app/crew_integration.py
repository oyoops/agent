from crewai import Agent, Task, Crew, Process

class AICrewManager:
    def __init__(self, api_key, model_name, max_tokens, temperature):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.llm_config = {
            'model': self.model_name,
            'temperature': self.temperature
        }

        self.analyst = Agent(
            role='Data Analyst',
            goal='Analyze data and provide insights',
            backstory='Expert in data analysis with years of experience',
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm_config=self.llm_config
        )
        
        self.recommender = Agent(
            role='Recommendation Specialist',
            goal='Provide personalized recommendations',
            backstory='AI specialist in creating tailored suggestions',
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm_config=self.llm_config
        )

        self.sentiment_analyzer = Agent(
            role='Sentiment Analyst',
            goal='Analyze sentiment in text data',
            backstory='Expert in natural language processing and sentiment analysis',
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm_config=self.llm_config
        )


    def analyze_data(self, data):
        task = Task(
            description=f"Analyze the following data and provide insights: {data}",
            agent=self.analyst,
            expected_output="A detailed analysis of the provided data with key insights."
        )
        crew = Crew(
            agents=[self.analyst],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return result

    def get_recommendation(self, user_data):
        task = Task(
            description=f"Generate a personalized recommendation based on: {user_data}",
            agent=self.recommender,
            expected_output="A personalized recommendation based on the user data provided."
        )
        crew = Crew(
            agents=[self.recommender],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return result

    def analyze_sentiment(self, text):
        task = Task(
            description=f"Analyze the sentiment of the following text: {text}",
            agent=self.sentiment_analyzer,
            expected_output="A sentiment analysis of the provided text, categorizing it as positive, negative, or neutral."
        )
        crew = Crew(
            agents=[self.sentiment_analyzer],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return result