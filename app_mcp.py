import streamlit as st
import requests
import os
import ast
import json
from langchain_cohere import ChatCohere
from phi.agent import Agent,RunResponse
from phi.tools.googlesearch import GoogleSearch
from phi.model.cohere import CohereChat
from dotenv import load_dotenv
# mcp client dependencies
from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
chat = ChatCohere(cohere_api_key=cohere_api_key)

def get_user_input(prompt, options, key):
    """Allow user to select an option or enter a custom response."""
    selected = st.radio(prompt, list(options.keys()) + ["Other (Specify)"], key=f"radio_{key}")
    
    if selected == "Other (Specify)":
        return st.text_input("Please specify:", "", key=f"text_{key}")
    
    return selected

def ask_questions():
    st.title("📌 Personalized Learning Pathway for Data Science & ML")

    edu_options = {"Commerce": "A", "Arts": "B", "Science": "C"}
    edu = get_user_input("1️⃣ What is your educational background?", edu_options, key="edu")

    interest_options = {
        "Customer Behavior & Market Trends": "A", 
        "Healthcare & Patient Analytics": "B", 
        "Education & Learning Technologies": "C",
        "Operations & Supply Chain Optimization": "D",
        "HR & Employee Analytics": "E",
        "Creative & Content Analytics": "F",
        "Legal & Compliance Analytics": "G"
    }
    interest = get_user_input("2️⃣ What interests you the most?", interest_options, key="interest")

    comfort_options = {
        "Not very comfortable": "A", 
        "Understand basic statistics": "B", 
        "Love working with data & trends": "C"
    }
    comfort = get_user_input("3️⃣ How comfortable are you with numbers & data?", comfort_options, key="comfort")

    goal_options = {
        "Career growth in current field": "A", 
        "Switching to a new domain": "B", 
        "Learning for self-improvement": "C"
    }
    goal = get_user_input("4️⃣ What is your current goal?", goal_options, key="goal")

    learning_style_options = {
        "Videos & Online Courses": "A",
        "Books & Research Papers": "B",
        "Hands-on Projects": "C"
    }
    learning_style = get_user_input("5️⃣ Preferred learning style?", learning_style_options, key="learning_style")

    time_per_week = st.slider("⏳ How many hours per week can you dedicate?", 5, 40, 10)

    salary = st.text_input("💰 Current Salary (if applicable, enter amount in Indian Rupees):", "")
    salary = salary if salary.strip() else "0"

    with open("user_responses.txt", "w") as file:
        file.write(f"Educational Background: {edu}\n")
        file.write(f"Interest: {interest}\n")
        file.write(f"Comfort with Data: {comfort}\n")
        file.write(f"Goal: {goal}\n")
        file.write(f"Learning Style: {learning_style}\n")
        file.write(f"Hours per Week: {time_per_week}\n")
        file.write(f"Current Salary: {salary}\n")

    if st.button("Submit Responses"):
        st.session_state["submitted"] = True
        
    return edu, interest, comfort, goal, learning_style, time_per_week, salary

# Handling MCP requests
async def run(user_data):
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            response = await session.call_tool("career_advice", arguments={"user_details":user_data})
            return response.content[0].text
        
async def roadmap_generator(career, selected_specialization, time_per_week, current_salary):
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            roadmap = await session.call_tool("roadmap_generator", arguments={"career":career,"specialization":selected_specialization,
                                                                               "time":time_per_week,"salary":current_salary})
            return roadmap.content[0].text
        
async def fetch_study_material(selected_specialization):
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            study_material = await session.call_tool("fetch_study_material", arguments={"subject":selected_specialization})
            return study_material.content[0].text

async def fetch_jobs(career):
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            jobs = await session.call_tool("fetch_jobs", arguments={"career":career})
            return jobs.content[0].text
        
async def get_current_location():
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            study_material = await session.call_tool("get_current_location")
            return study_material.content[0].text
        
async def beautify_prompt(roadmap):
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            output = await session.get_prompt(
                "beautify", arguments={"message":roadmap}
             )
            return output
        
def show_dashboard():
    """Displays the dynamic dashboard after user submission."""
    if "submitted" in st.session_state and st.session_state["submitted"]:
        # Read updated user data
        with open("user_responses.txt", 'r') as file:
            user_data = file.read()

        # Dynamically invoke counselor after submission
        response = ast.literal_eval(asyncio.run(run(user_data))) 

        st.title("🚀 Personalized Career Pathway Dashboard")
        st.subheader(f"**Career Suggestion: {response['career']}**")
        st.write(response["description"])

        # Specialization Selection
        st.subheader("📚 Available Specializations")
        selected_specialization = st.selectbox(
            "Select a specialization you're interested in:",
            response["specializations"],
            key="specialization"
        )

        # Only generate roadmap if a specialization is selected
        if selected_specialization:
            # Retrieve user details for roadmap
            career = response["career"]
            time_per_week = st.session_state.get("time_per_week", 10)
            current_salary = st.session_state.get("salary", "0lpa")

            # Call roadmap_generator and store response
            if "roadmap_data" not in st.session_state or st.session_state["selected_specialization"] != selected_specialization:
                st.session_state["roadmap_data"] = ast.literal_eval(asyncio.run(roadmap_generator(career, selected_specialization, time_per_week, current_salary)))
                st.session_state["selected_specialization"] = selected_specialization  # Store the last chosen specialization

            roadmap = st.session_state["roadmap_data"]

            # Display roadmap details
            st.subheader("🛤️ Your Personalized Learning Roadmap")
            st.markdown(chat.invoke(asyncio.run(beautify_prompt(roadmap['roadmap'])).messages[0].content.text).content)
            st.markdown(f"**🛠 Tools & Skills Required:** {roadmap['tools and skills required']}")
            st.markdown(f"**📂 How to Build Your Portfolio:** {roadmap['how to create a portfolio and become job ready']}")
            st.markdown(f"**💰 Salary Hike Projection:** {roadmap['salary hike']}")

            if st.button("📚 Find Study Material"):
                study_material = asyncio.run(fetch_study_material(selected_specialization))
                st.subheader("📖 Study Material")
                st.write(study_material)

            if st.button("💰 Find Jobs"):
                jobs = asyncio.run(fetch_jobs(career))
                st.subheader(f"📖 Jobs near {asyncio.run(get_current_location())}")
                st.write(jobs)            

def main():
    ask_questions()
    show_dashboard()
    # Display author information
    st.markdown("""
    ---
    **Coded by:** [Hrithik Rai Saxena](https://www.linkedin.com/in/hrithikraisaxena/), [Rishi Rai Saxena](https://www.linkedin.com/in/rishi-rai-saxena/)
    """)

if __name__ == "__main__":
    main()
    
