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

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
chat = ChatCohere(cohere_api_key=cohere_api_key)
chat_agent = CohereChat(api_key=cohere_api_key)

def get_current_location():
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        city= data.get("city", "Unknown"),
        
        return f"city {city[0]}"

agent = Agent(
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

def fetch_study_material(subject):
    response = agent.run(subject)
    return response.content

def fetch_jobs(career):
    response = job_agent.run(career)
    return response.content

example = {
    "career": "put career name",
    "description": "This role combines your interest in .... with your love for ....., leveraging .... to analyze ...... It’s a perfect bridge from a non-technical .... background to a technical AI-focused career.",
    "specializations": [
        "specializations 1",
        "specializations 2",
        "AI-specializations 3",
        "list further suitable specializations",
    ]
    }

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

def counselor(user_details):
    template = f'''
    You are a professional career counselor that talks to the user. Your job is to help transition the user into the field of Artificial Intelligence.
    Important - Answer to the point, keep it concise and only answer what is asked. 
    User profile - 
    {user_details}

    You will recieve a user profile, your job is to -
    1. Tell me a career that maps perfectly with the provided options given the user wants to transition from a non technical to a technical background.
    2. Tell me specializations that the user can do for the suggested career.

    Provide the answer in the following format like this example - 
    {example}
    '''
    response = chat.invoke(template).content
    return ast.literal_eval(response)


with open("user_responses.txt", 'r') as file:
    user_data = file.read()

# Placeholder for chatbot response
chatbot_response = counselor(user_data)

example_roadmap = {
    "roadmap": "write detailed roadmap here with each week progress (explained in detail) in bullet points.",
    "tools and skills required": "List them here",
    "how to create a portfolio and become job ready": "Detailed description",
    "salary hike" : "if available"
    }

def roadmap_generator(career, specialization, time, current_salary):
    template = f'''
    You are a professional career counselor, your client wants to pursue a career in {career},
    with specialization in {specialization}. Your client can only spare {time} hours per week to up skill,
    and client's current salary is Rs. {current_salary}/annum.

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

def show_dashboard():
    """Displays the dynamic dashboard after user submission."""
    if "submitted" in st.session_state and st.session_state["submitted"]:
        # Read updated user data
        with open("user_responses.txt", 'r') as file:
            user_data = file.read()

        # Dynamically invoke counselor after submission
        response = counselor(user_data)  

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
            current_salary = st.session_state.get("salary", "0")

            # Call roadmap_generator and store response
            if "roadmap_data" not in st.session_state or st.session_state["selected_specialization"] != selected_specialization:
                st.session_state["roadmap_data"] = roadmap_generator(career, selected_specialization, time_per_week, current_salary)
                st.session_state["selected_specialization"] = selected_specialization  # Store the last chosen specialization

            roadmap = st.session_state["roadmap_data"]

            # Display roadmap details
            st.subheader("🛤️ Your Personalized Learning Roadmap")
            st.markdown(chat.invoke(f"**📌 Roadmap:** {roadmap['roadmap']})").content)
            st.markdown(f"**🛠 Tools & Skills Required:** {roadmap['tools and skills required']}")
            st.markdown(f"**📂 How to Build Your Portfolio:** {roadmap['how to create a portfolio and become job ready']}")
            st.markdown(f"**💰 Salary Hike Projection:** {roadmap['salary hike']}")

            if st.button("📚 Find Study Material"):
                study_material = fetch_study_material(selected_specialization)
                st.subheader("📖 Study Material")
                st.write(study_material)

            if st.button("💰 Find Jobs"):
                study_material = fetch_jobs(career)
                st.subheader(f"📖 Jobs near {get_current_location()}")
                st.write(study_material)            

def main():
    ask_questions()
    show_dashboard()
    # Display author information
    st.markdown("""
    ---
    **Author:** [Rishi Rai Saxena](https://www.linkedin.com/in/rishi-rai-saxena/)
    """)

if __name__ == "__main__":
    main()
    
