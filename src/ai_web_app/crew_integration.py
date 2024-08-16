from crewai import Agent, Task, Crew, Process
from typing import Dict, Any, List

class AICrewManager:
    def __init__(self, api_key: str, model_name: str, max_tokens: int, temperature: float):
        self.api_key = api_key
        self.llm_config = {
            'model': model_name,
            'temperature': temperature,
            'max_tokens': max_tokens
        }

        # Initialize agents
        self.analyst = self._create_agent(
            'Data Analyst',
            'Analyze data and provide deep insights',
            'Expert in data analysis with years of experience in various fields'
        )
        self.recommender = self._create_agent(
            'Recommendation Specialist',
            'Provide personalized and context-aware recommendations',
            'AI specialist in creating tailored suggestions based on user preferences and behavior'
        )
        self.sentiment_analyzer = self._create_agent(
            'Sentiment Analyst',
            'Analyze sentiment in text data with nuanced understanding',
            'Expert in natural language processing and emotion detection in text'
        )
        self.content_creator = self._create_agent(
            'Content Creator',
            'Generate engaging and relevant content based on given topics or data',
            'Creative writer with expertise in various content formats and styles'
        )

    def _create_agent(self, role: str, goal: str, backstory: str) -> Agent:
        """Helper method to create an agent with common configurations."""
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=False,
            llm_config=self.llm_config
        )

    def _run_crew_task(self, agent: Agent, task_description: str, expected_output: str) -> Dict[str, Any]:
        """Helper method to run a single task with a crew."""
        task = Task(
            description=task_description,
            agent=agent,
            expected_output=expected_output
        )
        crew = Crew(agents=[agent], tasks=[task], verbose=True)  # Changed from 2 to True
        return crew.kickoff()

    def analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self._run_crew_task(
            self.analyst,
            f"Analyze the following data and provide comprehensive insights: {data}. "
            f"Consider trends, anomalies, and potential implications.",
            "A detailed analysis report with key insights, trends, and recommendations."
        )
        return {"analysis": result}

    def get_recommendation(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        result = self._run_crew_task(
            self.recommender,
            f"Generate personalized recommendations based on: {user_data}. "
            f"Consider user preferences, past behavior, and current trends.",
            "A list of tailored recommendations with explanations for each suggestion."
        )
        return {"recommendations": result}

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        result = self._run_crew_task(
            self.sentiment_analyzer,
            f"Analyze the sentiment of the following text: '{text}'. "
            f"Provide a nuanced analysis, considering context and subtle emotional cues.",
            "A detailed sentiment analysis including overall sentiment, confidence score, and key emotional indicators."
        )
        return {"sentiment_analysis": result}
   

    def generate_content(self, topic: str, content_type: str) -> Dict[str, Any]:
        task = Task(
            description=f"Create {content_type} content about the following topic: '{topic}'. "
                        f"Ensure the content is engaging, informative, and tailored to the specified content type.",
            agent=self.content_creator,
            expected_output=f"Original {content_type} content related to the given topic."
        )
        crew = Crew(agents=[self.content_creator], tasks=[task], verbose=True)
        result = crew.kickoff()
        
        return {
            "generated_content": result.task_output,
            "topic": topic,
            "content_type": content_type
        }

    def comprehensive_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tasks = [
            Task(
                description=f"Analyze the following data: {data}. Provide comprehensive insights.",
                agent=self.analyst,
                expected_output="Detailed data analysis report."
            ),
            Task(
                description="Based on the analysis, determine the overall sentiment of the data.",
                agent=self.sentiment_analyzer,
                expected_output="Sentiment analysis of the data insights."
            ),
            Task(
                description="Using the analysis and sentiment, generate strategic recommendations.",
                agent=self.recommender,
                expected_output="Strategic recommendations based on data analysis and sentiment."
            ),
            Task(
                description="Create a summary report of all findings and recommendations.",
                agent=self.content_creator,
                expected_output="Engaging summary report of analysis, sentiment, and recommendations."
            )
        ]

        crew = Crew(
            agents=[self.analyst, self.sentiment_analyzer, self.recommender, self.content_creator],
            tasks=tasks,
            verbose=2
        )
        result = crew.kickoff()
        return {"comprehensive_analysis": result}