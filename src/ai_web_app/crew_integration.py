from crewai import Agent, Task, Crew, Process

class AICrewManager:
    def __init__(self):
        self.analyst = Agent(
            role='Data Analyst',
            goal='Analyze data and provide insights',
            backstory='Expert in data analysis with years of experience'
        )
        
        self.recommender = Agent(
            role='Recommendation Specialist',
            goal='Provide personalized recommendations',
            backstory='AI specialist in creating tailored suggestions'
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