import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat, MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
# Access your key
openai_api_key = os.getenv("OPENAI_API_KEY")
async def main():
    filesystem_server_params = StdioServerParams(command="npx",
                                                 args=[
                                                     "-y",
                                                     "@modelcontextprotocol/server-filesystem",
                                                     "D:/AgenticAIProject"],
                                                 read_timeout_seconds=60

                                                 )
    fs_workbench = McpWorkbench(filesystem_server_params)
    async with fs_workbench as fs_wb:
        openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-2024-08-06")
        machine=AssistantAgent(name="MathTutor", model_client=openai_model_client, workbench=fs_wb, system_message="You are a math teacher, and when human ask to do some math calculation give the answer correctly. Kindly terminate the chat when user writes 'END CHAT. and reply with 'LESSON COMPLETE'")
        Useragent=UserProxyAgent(name="HumanAgent")
        team=RoundRobinGroupChat(participants=[Useragent,machine],termination_condition=TextMessageTermination("END CHAT"))
        await Console(team.run_stream(task="Help me with multiplication problem. Feel Free to create files to help the student with more details"))
        await openai_model_client.close()
asyncio.run(main())