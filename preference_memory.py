from agno.agent.agent import Agent,AgentMemory
from agno.models.azure import AzureOpenAI
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.db import MemoryDb 

from config import api_key, api_endpoint, api_version, api_deployment

model = AzureOpenAI(api_key=api_key,azure_endpoint=api_endpoint,azure_deployment=api_deployment,api_version=api_version )

memory_db = SqliteMemoryDb(
    table_name="agent_memory",
    db_file="storage/agent_storage.db",
    
)
agent = Agent(
    model=model,
    memory=AgentMemory(
        db=memory_db,
        create_user_memories=True,
        update_user_memories_after_run=True,
        create_session_summary=True,
        update_session_summary_after_run=True
    ),
    storage=SqliteStorage(
        table_name='agent_sessions',
        db_file='storage/agent_storage.db'
    ),
    add_history_to_messages=True,
    num_history_responses=5,
    debug_mode=True,
    show_tool_calls=True
)

agent.print_response("Hi ,this is Sudar and I love coding",stream=True)
agent.print_response("I am studying in IITM",stream=True)

agent.print_response("What do you know about me?",stream=True)
