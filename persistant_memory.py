from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.storage.sqlite import SqliteStorage

from config import api_key, api_endpoint, api_version, api_deployment

model = AzureOpenAI(api_key=api_key,azure_endpoint=api_endpoint,azure_deployment=api_deployment,api_version=api_version )

# fbae7e88-099f-45de-8365-10bb9623ce59  


agent = Agent(
    model=model,
    storage = SqliteStorage(
        table_name='agent_sessions',
        db_file='storage/agent_storage.db'
    ),
   add_history_to_messages=True,
   session_id="fbae7e88-099f-45de-8365-10bb9623ce59"
)


# agent.print_response("Hi ,this is Sudar",stream=True)
# agent.print_response("I live in India ",stream=True)

agent.print_response("What is my name?",stream=True)

# print(agent.session_id)