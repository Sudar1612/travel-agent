from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.tools.math_toolkit import MathToolkit

from config import api_key, api_endpoint, api_version, api_deployment

model = AzureOpenAI(api_key=api_key,azure_endpoint=api_endpoint,azure_deployment=api_deployment,api_version=api_version )


agent = Agent(
    model=model,
    tools=[MathToolkit()],
    add_history_to_messages=True,
    show_tool_calls=True,
)

agent.print_response("Can we divide 54 by 0?", stream=True)