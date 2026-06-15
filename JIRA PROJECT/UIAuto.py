import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMessageTermination, MaxMessageTermination
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
jiraToken = os.getenv("JIRA_TOKEN")
jiraUsername = os.getenv("JIRA_USERNAME")
jirURL = os.getenv("JIRA_URL")
jiraProj = os.getenv("JIRA_PROJECT")


async def main():
    playwright_server_params = StdioServerParams(command="npx",
                                                 args=[
                                                     "@playwright/mcp@latest"],
                                                 read_timeout_seconds=60

                                                 )
    playwrightWorkbench = McpWorkbench(playwright_server_params)
    async with playwrightWorkbench as pw_wb:
        openai_model_client = OpenAIChatCompletionClient(
            model="gpt-4o-2024-08-06")
        auto_agent = AssistantAgent(name="AutomationAnalyst", model_client=openai_model_client, workbench=pw_wb,
                                    system_message="You are an automation agent which can perform UI actions by using locators from dom")
        human=UserProxyAgent(name="hAgent")
        rb = RoundRobinGroupChat(participants=[human, auto_agent],
                                 termination_condition=MaxMessageTermination(4))
        await Console(rb.run_stream(
            task="Take statements from human agent and perform UI actions on them",))
        await openai_model_client.close()


asyncio.run(main())
