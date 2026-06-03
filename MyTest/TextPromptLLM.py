import asyncio
import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
#creation of agent
# Load variables from .env
load_dotenv()
# Access your key
openai_api_key = os.getenv("OPENAI_API_KEY")
async def main():
    openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o-2024-08-06")
    agent=AssistantAgent(name="JayantAssistentAgent", model_client=openai_model_client)
    await Console(agent.run_stream(task="Where is mastercard in pune located"))
    await openai_model_client.close()
asyncio.run(main())