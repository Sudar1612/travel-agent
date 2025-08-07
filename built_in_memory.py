from agno.agent import Agent
from agno.models.azure import AzureOpenAI

from config import api_key, api_endpoint, api_version, api_deployment

model = AzureOpenAI(api_key=api_key,azure_endpoint=api_endpoint,azure_deployment=api_deployment,api_version=api_version )


agent = Agent(
    model=model,
    add_history_to_messages=True,
    num_history_responses=4
)

agent.print_response("Hi ,this is Sudar",stream=True)
agent.print_response("Hi ,I live in India ",stream=True)
agent.print_response("I am an AI Engineer",stream=True)
agent.print_response("Can you remember my name?",stream=True)