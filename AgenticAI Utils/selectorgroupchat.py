import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
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
    agent1 = AssistantAgent(name="MovieReasearchReview", model_client=openai_model_client,
                            system_message="Yo are movie reviewer with some research experience, you give logical reviews of a movie with considering the history of actor and director")
    agent2 = AssistantAgent(name="MovieWriteReviewAgent", model_client=openai_model_client,
                            system_message="You are a random movie reviewer with no experience, you write useless reviews of any movie")
    agent3 = AssistantAgent(name="CriticMovieAgent", model_client=openai_model_client,
                            system_message="You are a movie critic , you only give a verdict whether movie is good or bad")
    groupChat = SelectorGroupChat(participants=[agent2, agent3, agent1], model_client=openai_model_client,
                                  termination_condition=MaxMessageTermination(max_messages=10),
                                  allow_repeated_speaker=True)

    await Console(groupChat.run_stream(task="Lets discuss how the movie 'Pathan' is for the Indian audience"))
    await openai_model_client.close()


asyncio.run(main())
