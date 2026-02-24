import os
from corporative_agent.crew import MultiAgentPlatform
from dotenv import load_dotenv

def run():
    question = input("\nUsuário: ")

    crew_instance = MultiAgentPlatform().crew()
    print(crew_instance)

    result = crew_instance.kickoff(
        inputs={
            "user_question": question
        }
    )

    print("\nAgente:\n")
    print(result)


if __name__ == "__main__":
    load_dotenv()
    run()