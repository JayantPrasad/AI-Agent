import asyncio
import json
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
    helperAgent = AssistantAgent(name="Helper", model_client=openai_model_client)
    backuphelper = AssistantAgent(name="BackupHelper", model_client=openai_model_client)
    await Console(helperAgent.run_stream(task="My favourite sport is cricket"))
    state = await helperAgent.save_state()
    with open("mycontent.json", "w") as f:
        json.dump(state, f, default=str)
    with open("mycontent.json", "r") as f:
        saved_state = json.load(f)
    await backuphelper.load_state(saved_state)

    await Console(backuphelper.run_stream(task="What is my favourite sport?"))
    await openai_model_client.close()


asyncio.run(main())
