import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
# Access your key
openai_api_key = os.getenv("OPENAI_API_KEY")
async def main():
    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-2024-08-06")
    autoAgent=MultimodalWebSurfer(name="WebAutomation",model_client=openai_model_client,headless=False,animate_actions=True)
    actionVar=RoundRobinGroupChat(participants=[autoAgent],max_turns=3)
    await Console(actionVar.run_stream(task="Search Mastercard office in pune in google chrome, tell me the count of reviews and how far it is from Pune Airport"))


    await openai_model_client.close()
asyncio.run(main())