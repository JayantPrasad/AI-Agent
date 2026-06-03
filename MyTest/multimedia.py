import asyncio
import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load variables from .env
load_dotenv()
# Access your key
openai_api_key = os.getenv("OPENAI_API_KEY")

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")
    multimodalagent=AssistantAgent(name="MultiModalAgent", model_client=openai_model_client)
    image=Image.from_file("D:/AI Agent/Image Files/merry-christmas-and-a-happy-new-year-2-1.jpg")
    messageimage=MultiModalMessage(
        content=["what do you see in the image",image],source="user"
    )
    await Console(multimodalagent.run_stream(task=messageimage))
    await multimodalagent.close()


asyncio.run(main())
