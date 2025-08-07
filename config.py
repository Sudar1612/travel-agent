import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
api_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")