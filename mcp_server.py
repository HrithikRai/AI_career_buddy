from mcp.server.fastmcp import FastMCP
import requests
import os
import ast
import json
from langchain_cohere import ChatCohere
from phi.agent import Agent, RunResponse
from phi.tools.googlesearch import GoogleSearch
from phi.model.cohere import CohereChat
from dotenv import load_dotenv

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
chat_agent = CohereChat(api_key=cohere_api_key)
chat = ChatCohere(cohere_api_key=cohere_api_key)


mcp = FastMCP("AI Career Assistant Server")

@mcp.tool()
def get_current_location():
        """Fetches current location of the user"""
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        city= data.get("city", "Unknown"),
        
        return f"city {city[0]}"

study_agent = Agent(
    provider=chat_agent,
    tools=[GoogleSearch()],
    description=f"You are a friendly youtube video link provider to assist in study for the desired subjects",
    instructions=[
        "Given subject names provide links in https format",
        "provide atleast 5 links and cover almost every subject",
        "Search in English and make sure to get youtube links and all relevant references",
        "provid the answer in a friendly manner for example, Hey there, I've created a personalised list consisting of the following -"
    ],
)

job_agent = Agent(
    provider=chat_agent,
    tools=[GoogleSearch()],
    description=f"You are a job finder buddy, help find available jobs in {get_current_location()} region of the mentioned job title",
    instructions=[
        "Given a request provide relevant job links in https format",
        "provide atleast 5 job links with description",
        "Search in English",
    ],
)

@mcp.tool()
def fetch_study_material(subject: str) -> str:
    """Fetches study material YouTube links for the given subject."""
    response = study_agent.run(subject)
    return response.content

@mcp.tool()
def fetch_jobs(career: str) -> str:
    """Fetches job listings based on the given career title."""
    response = job_agent.run(career)
    return response.content

career_counselor_output_example = {
    "career": "put career name",
    "description": "This role combines your interest in .... with your love for ....., leveraging .... to analyze ...... It’s a perfect bridge from a non-technical .... background to a technical AI-focused career.",
    "specializations": [
        "specializations 1",
        "specializations 2",
        "AI-specializations 3",
        "list further suitable specializations",
    ]
    }

# dynamic resource, static resources availbale too
@mcp.tool()
def career_advice(user_details: str) -> dict:
    """Provides professional career advice"""
    template = f'''
        You are a professional career counselor that talks to the user. Your job is to help transition the user into the field of Artificial Intelligence.
        Important - Answer to the point, keep it concise and only answer what is asked. 
        User profile - 
        {user_details}

        You will recieve a user profile, your job is to -
        1. Tell me a career that maps perfectly with the provided options given the user wants to transition from a non technical to a technical background.
        2. Tell me specializations that the user can do for the suggested career.

        Provide the answer in the following format like this example - 
        {career_counselor_output_example}
        '''
    response = chat.invoke(template).content
    return ast.literal_eval(response)

example_roadmap = {
    "roadmap": "write detailed roadmap here with each week progress (explained in detail) in bullet points.",
    "tools and skills required": "List them here",
    "how to create a portfolio and become job ready": "Detailed description",
    "salary hike" : "if available"
    }

@mcp.tool()
def roadmap_generator(career: str, specialization: str, time: int, salary: str) -> dict:
    """Creates a roadmap for the selected specialization"""
    template = f'''
    You are a professional career counselor, your client wants to pursue a career in {career},
    with specialization in {specialization}. Your client can only spare {time} hours per week to up skill,
    and client's current salary is Rs. {salary}/annum.

    Your job is to:
    1. Generate a specialized roadmap adhering strictly to the specialization and time mentioned.
    2. List all the necessary tools and skills required.
    3. Suggest how to create a portfolio, so that client can become job ready.
    4. Expected salary hike if the client switches into new role if current annual salary provided.

    Provide the answer strictly in curly braces without using any special characters - 
    {example_roadmap}

    '''
    response = chat.invoke(template).content
    return ast.literal_eval(response.replace("\n",""))

@mcp.prompt()
def beautify(message: str) -> str:
    """Create a prompt to beautify roadmap output"""
    return f"Roadmap in chronological order: {message}"

if __name__ == "__main__":
    # Start a process that communicates via standard input/output
    mcp.run(transport="sse")
