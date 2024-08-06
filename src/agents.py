from langchain_community.llms import Ollama
from crewai import Agent

# Initialize LLM
llm = Ollama(model="llama3.1:latest")

# Define Agents
intent_mapper_agent = Agent(
    role='Intent Mapper',
    goal='Extract travel intent information from user query',
    backstory="You are responsible for understanding and extracting key details from travel-related queries.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

finder_agent = Agent(
    role='Finder',
    goal='Find top travel recommendations based on user intent',
    backstory="You find the best travel options based on user's requirements.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

itinerary_maker_agent = Agent(
    role='Itinerary Maker',
    goal='Create a detailed itinerary including spots, activities and eateries nearby the user selected stay based on user interest',
    backstory="""
    You prepare comprehensive travel itineraries based on user interests. 
    you do extensive research to figure out which tourists spots,activities, eateries would best suit the user interest
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm
)
