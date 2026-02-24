from corporative_agent.crew import MultiAgentPlatform
from dotenv import load_dotenv

def run():
    question = input("Faça sua pergunta: ")

    crew_instance = MultiAgentPlatform().crew()
    result = crew_instance.kickoff(inputs={"user_question": question})

    print(f"\nResposta: {result}")

if __name__ == "__main__":
    load_dotenv()
    run()