import sys

from typing import List
from textwrap import dedent
from pydantic import BaseModel, Field
from rich.prompt import Prompt

from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.tools.exa import ExaTools
from agno.tools.duckduckgo import DuckDuckGoTools

from map_tools import GoogleMapsTool
from prompts import system_prompt_travel_agent,expected_output,instructions


 
EXA_API_KEY = 'AIzaSyAKnhvpcKTcxE3aaIv5BHzBfhQ1OaNuRdk'
MAPS_API_KEY = 'af427766-3a25-4c54-aec8-f68938e2525d'

AZURE_OPENAI_API_KEY="605566d0ec2247c2931469a31bdbbf5a"
AZURE_OPENAI_ENDPOINT="https://botminds-alpha-ai.openai.azure.com/"
AZURE_OPENAI_API_VERSION="2023-03-15-preview"
AZURE_OPENAI_DEPLOYMENT="gpt-4o"

# data models
class MapURL(BaseModel):
    place_name : str = Field(None, description="The name of the place to search for")
    maps_url : str = Field(None, description="Google Maps URL for the place")

class MapsURLs(BaseModel):
    urls : List[MapURL]

class Inputs(BaseModel):
    days : int = Field(None , description="No of days for the trip")
    destination : str = Field(None, description="The destination of the trip")
    trip_data : str = Field(None, description="The date of the trip")
    budget : int = Field(None , description="The total budget for the trip")


model = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY,azure_endpoint=AZURE_OPENAI_ENDPOINT,azure_deployment=AZURE_OPENAI_DEPLOYMENT,api_version=AZURE_OPENAI_API_VERSION )


# agents
travel_planning_agent = Agent(
    name='Travel Planning Agent',
    model=model,
    tools=[ExaTools(api_key=EXA_API_KEY)],
    description=system_prompt_travel_agent,
    instructions=instructions, 
    expected_output=expected_output,
    add_datetime_to_instructions=True,
    debug_mode=False
)

map_agent = Agent(
    name = 'Google Map Agent',
    model = model,
    description="You are equipped with Google Map tools to extract place ID ",
    tools = [GoogleMapsTool(api_key=MAPS_API_KEY)],
    debug_mode=False
)


duckduckgo_agent = Agent(
    name = "DuckDuckGo Agent",
    model = model,
    description="You are equipped with DuckDuckGo tools to help with searching business info on the web",
    tools = [DuckDuckGoTools()],
    show_tool_calls = False,
    debug_mode=True
)

team_agent = Agent(
    model=model,
    team=[travel_planning_agent,map_agent,duckduckgo_agent],
    add_history_to_messages=True,
    description=dedent('''
You are now connected to the Travel Planning Agent , Google Maps Agnet , and  DuckDuckGo agent.
                       The Travel Planning Agent will help you generate an initial itinerary based on your input.
                       The Google Maps Agent will help you extract Google Maps URLs for accomdatation and activities.
                       The DuckDuckGo Agent will help you fill in any missign information about the business and landmakrs idejtified in the itinerary.
'''),
instructions=dedent('''
# Travel Planning Agent Instructions
                    
                    ## 1. Generate the initial itinerary from travel planning agent based on the user's input.
                    ## 2. Go through the itinerary and ensure that all location adn landmarks have Google Map URLs included.
                    ## 3. Use the DuckDuckGo Agent to fill any missing information about business and landmarks identified in the itinerary.
'''),
expected_output=expected_output,
markdown=True,
show_tool_calls=True
)

if __name__ == '__main__':
    while True:
        user_prompt = Prompt.ask('User')
        if user_prompt =='exit' or user_prompt == 'quit':
            sys.exit('Ba Bye!')
        team_agent.print_response(user_prompt,stream=True)