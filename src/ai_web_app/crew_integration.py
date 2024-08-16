from crewai import Agent, Task, Crew, Process
from typing import Dict, Any

class AICrewManager:
    def __init__(self, api_key: str, model_name: str, max_tokens: int, temperature: float):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.analyst = Agent(
            role='Data Analyst',
            goal='Analyze data and provide deep insights',
            backstory='Expert in data analysis with years of experience in various fields',
            verbose=True,
            allow_delegation=False,
            llm_config={
                'model': self.model_name,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
        )
        
        self.recommender = Agent(
            role='Recommendation Specialist',
            goal='Provide personalized and context-aware recommendations',
            backstory='AI specialist in creating tailored suggestions based on user preferences and behavior',
            verbose=True,
            allow_delegation=False,
            llm_config={
                'model': self.model_name,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
        )

        self.sentiment_analyzer = Agent(
            role='Sentiment Analyst',
            goal='Analyze sentiment in text data with nuanced understanding',
            backstory='Expert in natural language processing and emotion detection in text',
            verbose=True,
            allow_delegation=False,
            llm_config={
                'model': self.model_name,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
        )

        self.content_creator = Agent(
            role='Content Creator',
            goal='Generate engaging and relevant content based on given topics or data',
            backstory='Creative writer with expertise in various content formats and styles',
            verbose=True,
            allow_delegation=False,
            llm_config={
                'model': self.model_name,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
        )

    def analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        task = Task(
            description=f"Analyze the following data and provide comprehensive insights: {data}. "
                        f"Consider trends, anomalies, and potential implications.",
            agent=self.analyst,
            expected_output="A detailed analysis report with key insights, trends, and recommendations."
        )
        crew = Crew(
            agents=[self.analyst],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return {"analysis": result}

    def get_recommendation(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        task = Task(
            description=f"Generate personalized recommendations based on: {user_data}. "
                        f"Consider user preferences, past behavior, and current trends.",
            agent=self.recommender,
            expected_output="A list of tailored recommendations with explanations for each suggestion."
        )
        crew = Crew(
            agents=[self.recommender],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return {"recommendations": result}

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        task = Task(
            description=f"Analyze the sentiment of the following text: '{text}'. "
                        f"Provide a nuanced analysis, considering context and subtle emotional cues.",
            agent=self.sentiment_analyzer,
            expected_output="A detailed sentiment analysis including overall sentiment, confidence score, and key emotional indicators."
        )
        crew = Crew(
            agents=[self.sentiment_analyzer],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return {"sentiment_analysis": result}

    def generate_content(self, topic: str, content_type: str) -> Dict[str, Any]:
        task = Task(
            description=f"Create {content_type} content about the following topic: '{topic}'. "
                        f"Ensure the content is engaging, informative, and tailored to the specified content type.",
            agent=self.content_creator,
            expected_output=f"Original {content_type} content related to the given topic."
        )
        crew = Crew(
            agents=[self.content_creator],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return {"generated_content": result}

    def comprehensive_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        analysis_task = Task(
            description=f"Analyze the following data: {data}. Provide comprehensive insights.",
            agent=self.analyst,
            expected_output="Detailed data analysis report."
        )
        sentiment_task = Task(
            description="Based on the analysis, determine the overall sentiment of the data.",
            agent=self.sentiment_analyzer,
            expected_output="Sentiment analysis of the data insights."
        )
        recommendation_task = Task(
            description="Using the analysis and sentiment, generate strategic recommendations.",
            agent=self.recommender,
            expected_output="Strategic recommendations based on data analysis and sentiment."
        )
        content_task = Task(
            description="Create a summary report of all findings and recommendations.",
            agent=self.content_creator,
            expected_output="Engaging summary report of analysis, sentiment, and recommendations."
        )

        crew = Crew(
            agents=[self.analyst, self.sentiment_analyzer, self.recommender, self.content_creator],
            tasks=[analysis_task, sentiment_task, recommendation_task, content_task],
            verbose=2
        )
        result = crew.kickoff()
        return {"comprehensive_analysis": result}