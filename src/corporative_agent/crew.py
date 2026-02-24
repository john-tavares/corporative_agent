from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import PDFSearchTool
from typing import List

@CrewBase
class MultiAgentPlatform:

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"]
        )

    @agent
    def compliance_guardian(self) -> Agent:
        return Agent(
            config=self.agents_config["compliance_guardian"]
        )
    
    @agent
    def knowledge_expert(self) -> Agent:
        pdf_tool = PDFSearchTool(pdf='././knowledge/condicao_de_acionamento.pdf')
        return Agent(
            config=self.agents_config["knowledge_expert"],
            allow_delegation=False,
            tools=[pdf_tool]
        )

    @agent
    def final_answer_compiler(self) -> Agent:
        return Agent(
            config=self.agents_config["final_answer_compiler"],
            allow_delegation=False
        )

    @task
    def compliance_task(self) -> Task:
        return Task(
            config=self.tasks_config["compliance_task"]
        )
    
    @task
    def rag_answer_task(self) -> Task:
        return Task(
            config=self.tasks_config["rag_answer_task"]
        )
    
    @task
    def final_answer_task(self) -> Task:
        return Task(
            config=self.tasks_config["final_answer_task"]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.manager(),
            memory=True,
            verbose=False,
            tracing=False
        )

    def kickoff(self, inputs: dict):
        return self.crew().kickoff(inputs=inputs)