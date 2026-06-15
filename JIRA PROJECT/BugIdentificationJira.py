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
    jira_server_params = StdioServerParams(command="docker",
                                           args=[
                                               "run", "-i", "--rm",
                                               "-e", f"JIRA_URL={jirURL}",
                                               "-e", f"JIRA_USERNAME={jiraUsername}",
                                               "-e", f"JIRA_API_TOKEN={jiraToken}",
                                               "-e", f"JIRA_PROJECTS_FILTER={jiraProj}",
                                               "ghcr.io/sooperset/mcp-atlassian:latest"
                                           ],
                                           read_timeout_seconds=60
                                           )

    jiraWorkbench = McpWorkbench(jira_server_params)
    playwright_server_params = StdioServerParams(command="npx",
                                                 args=[
                                                     "@playwright/mcp@latest"],
                                                 read_timeout_seconds=60

                                                 )
    playwrightWorkbench = McpWorkbench(playwright_server_params)
    async with jiraWorkbench as jira_wb, playwrightWorkbench as pw_wb:
        openai_model_client = OpenAIChatCompletionClient(
            model="gpt-4o-2024-08-06")
        bug_analyst_agent = AssistantAgent(name="BugAnalyst", model_client=openai_model_client, workbench=jira_wb,
                                           system_message="You are a jira agemt which can search the number of bugs in the project and give me output in numbers")
        auto_agent = AssistantAgent(name="AutomationAnalyst", model_client=openai_model_client, workbench=pw_wb,
                                    system_message="You are an automation agent which can perform UI actions by using locators from dom")
        rb = RoundRobinGroupChat(participants=[bug_analyst_agent, auto_agent],
                                 termination_condition=MaxMessageTermination(20))
        await Console(rb.run_stream(
            task="In JIRA go to my My project 'MYP' search the number of bugs in the project and automate the steps and give a good report to the user"))
        await openai_model_client.close()


asyncio.run(main())
