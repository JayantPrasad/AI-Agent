import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMessageTermination
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
    agent=AssistantAgent(name="HumanChat",model_client=openai_model_client,system_message="you are a helpful math teacher, you need to answer human queries which are related to maths. When user says 'END CHAT',acknowlege and say 'LESSON COMPLETE' and stop the chat")
    humanagent=UserProxyAgent(name="Human")
    chatbot=RoundRobinGroupChat(participants=[humanagent,agent],termination_condition=TextMessageTermination("LESSON COMPLETE"))
    await Console(chatbot.run_stream(task="I need an answer what is the value of 25 multipled by 2."))
    await openai_model_client.close()
asyncio.run(main())