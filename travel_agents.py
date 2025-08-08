import sys
import os

from dotenv import load_dotenv
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

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
api_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

exa_api_key = os.getenv("EXA_API_KEY")
maps_api_key = os.getenv("MAPS_API_KEY")


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


model = AzureOpenAI(api_key=api_key,azure_endpoint=api_endpoint,azure_deployment=api_deployment,api_version=api_version )


# agents
travel_planning_agent = Agent(
    name='Travel Planning Agent',
    model=model,
    tools=[ExaTools(api_key=exa_api_key)],
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
    tools = [GoogleMapsTool(api_key=maps_api_key)],
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