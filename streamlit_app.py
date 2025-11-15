import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM

# --- Page Configuration ---
st.set_page_config(
    page_title="CrewAI Multi-Agent System",
    page_icon="🤖",
    layout="wide"
)

# --- Sidebar for API Key ---
st.sidebar.title("🔑 Configuration")
api_key = st.sidebar.text_input("Enter your GOOGLE_API_KEY:", type="password")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    st.sidebar.success("API Key set successfully!")
else:
    st.sidebar.info("Please enter your GOOGLE_API_KEY to run the crew.")

# --- Main Application ---
st.title("🤖 Multi-Agent Orchestration System")
st.subheader("Powered by CrewAI & Google Gemini")
st.write("Enter a high-level goal, and the agent crew will work together to achieve it.")

# --- User Input ---
user_goal = st.text_area(
    "Enter your goal here:",
    placeholder="e.g., 'Write a 500-word blog post on the top 3 new trends in the EV industry for 2025.'",
    height=150
)

# --- Run Button ---
if st.button("🚀 Run Crew"):
    if not api_key:
        st.error("Please enter your GOOGLE_API_KEY in the sidebar to continue.")
    elif not user_goal:
        st.error("Please enter a goal for the crew.")
    else:
        with st.spinner("Crew is at work... 🧠"):
            try:
                # --- 1. Initialize the LLM ---
                gemini_model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
                llm = LLM(
                    model=f"gemini/{gemini_model_name}",
                    api_key=os.environ.get("GOOGLE_API_KEY")
                )

                # --- 2. Define Agents (Same as before) ---
                planner_agent = Agent(
                    role='Blog Post Planner',
                    goal='Take a high-level topic and create a detailed, structured outline for a blog post.',
                    backstory=(
                        "You are a master content strategist. You excel at taking a simple idea "
                        "and breaking it down into a logical, compelling structure."
                    ),
                    verbose=True,
                    allow_delegation=False,
                    llm=llm
                )
                
                researcher_agent = Agent(
                    role='Market Researcher',
                    goal='Find the latest, most relevant information on a given set of topics.',
                    backstory=(
                        "You are a skilled researcher, capable of sifting through noise to find "
                        "the signal. You can quickly gather facts, figures, and trends."
                    ),
                    verbose=True,
                    allow_delegation=False,
                    llm=llm
                )
                
                writer_agent = Agent(
                    role='Content Writer',
                    goal='Write a compelling, easy-to-read blog post from a given outline and research.',
                    backstory=(
                        "You are a professional blog post writer. You can take a structured outline "
                        "and research findings and weave them into an engaging narrative."
                    ),
                    verbose=True,
                    allow_delegation=False,
                    llm=llm
                )

                # --- 3. Define Tasks (Using the user_goal) ---
                task_plan = Task(
                    description=(
                        f"Create a detailed blog post outline for the topic: '{user_goal}'. "
                        "The outline must include: "
                        "1. An engaging title. "
                        "2. A brief introduction. "
                        "3. Three main sections, one for each trend/topic. "
                        "4. For each section, list 2-3 specific questions to research. "
                        "5. A concluding paragraph summary."
                    ),
                    expected_output="A structured markdown outline with title, intro, 3 main points (with sub-questions), and a conclusion.",
                    agent=planner_agent
                )
                
                task_research = Task(
                    description=(
                        "Using the blog post outline provided, conduct research to answer all "
                        "the specific sub-questions in the outline. "
                        "Find at least one key fact or statistic for each of the three main sections."
                    ),
                    expected_output="A report of research findings, clearly organized by the outline's main points.",
                    agent=researcher_agent,
                    context=[task_plan]
                )
                
                task_write = Task(
                    description=(
                        "Write the full blog post using the provided outline and research findings. "
                        "The post must be approximately 500 words. "
                        "It should be engaging, informative, and "
                        "follow the structure of the plan. "
                        "Directly use the research data to support your points."
                    ),
                    expected_output=f"A complete, formatted blog post of ~500 words on the topic '{user_goal}'.",
                    agent=writer_agent,
                    context=[task_plan, task_research]
                )

                # --- 4. Create and Run the Crew ---
                ev_trends_crew = Crew(
                    agents=[planner_agent, researcher_agent, writer_agent],
                    tasks=[task_plan, task_research, task_write],
                    process=Process.sequential,
                    verbose=True # Logs will appear in the terminal, not the UI
                )
                
                # Kick off the crew
                result = ev_trends_crew.kickoff()
                
                # --- 5. Display Result ---
                st.success("Crew finished the task!")
                st.markdown("---")
                st.header("Final Output:")
                st.markdown(result)

            except Exception as e:
                st.error(f"An Error Occurred: {e}")
                st.error("Please ensure your API key is correct and has the necessary permissions.")