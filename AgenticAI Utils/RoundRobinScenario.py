import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
# Access your key
openai_api_key = os.getenv("OPENAI_API_KEY")
async def main():
    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-2024-08-06")
    calculationAgent1=AssistantAgent(name="Calculation",model_client=openai_model_client,
                               system_message="You are a math teacher, explain concepts in details and some follow up questions.")
    studentagent2=AssistantAgent(name="Student",model_client=openai_model_client,
                               system_message="You are a student, ask questions")
    team=RoundRobinGroupChat(participants=[calculationAgent1,studentagent2],termination_condition=MaxMessageTermination(max_messages=6))
    await Console(team.run_stream(task="Lets discuss division and multiplication"))
    await openai_model_client.close()

asyncio.run(main())