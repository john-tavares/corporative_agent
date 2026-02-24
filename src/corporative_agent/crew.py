import json
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import RagTool


@CrewBase
class MultiAgentPlatform:

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["strategy_manager"]
        )

    @agent
    def compliance_guardian(self) -> Agent:
        return Agent(
            config=self.agents_config["compliance_guardian"]
        )

    @agent
    def direct_response_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["direct_response_specialist"]
        )
    
    @agent
    def knowledge_expert(self) -> Agent:
        rag_tool = RagTool()
        rag_tool.add(data_type="file", path="knowledge/condicao_de_acionamento.pdf")
        return Agent(
            config=self.agents_config["knowledge_expert"],
            allow_delegation=False,
            tools=[rag_tool]
        )

    @task
    def compliance_task(self) -> Task:
        return Task(
            config=self.tasks_config["compliance_task"]
        )
    
    @task
    def direct_answer_task(self) -> Task:
        return Task(
            config=self.tasks_config["direct_answer_task"]
        )
    
    @task
    def rag_answer_task(self) -> Task:
        return Task(
            config=self.tasks_config["rag_answer_task"]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            memory=True,
            manager_agent=self.manager(),
            verbose=False,
            tracing=False
        )

    def kickoff(self, inputs: dict):
        return self.crew().kickoff(inputs=inputs)