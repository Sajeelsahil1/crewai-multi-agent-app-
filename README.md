🤖 Multi-Agent Orchestration System

This project is a simple web application that demonstrates a multi-agent orchestration system. It uses CrewAI to manage a team of AI agents (Planner, Researcher, and Writer) who collaborate to achieve a complex goal set by the user.

The application is built with Streamlit and powered by Google's Gemini language model.

This project was built to fulfill the task below:

✨ Features

Simple UI: A clean Streamlit interface to input your goal and API key.

Multi-Agent Crew: Demonstrates a 3-agent (Planner, Researcher, Writer) sequential workflow.

Dynamic Goal Setting: You provide the high-level goal, and the crew builds everything from scratch.

Powered by Gemini: Uses Google's Gemini API (via CrewAI's LLM class) as the "brain" for the agents.

🚀 How to Run

1. Clone the Repository

git clone [https://github.com/Sajeelsahil1/crewai-multi-agent-app.git](https://github.com/Sajeelsahil1/crewai-multi-agent-app.git)
cd YOUR_REPOSITORY_NAME


2. Install Dependencies

Create a virtual environment (recommended) and install all the required libraries from requirements.txt.

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install libraries
pip install -r requirements.txt


3. Get Your API Key

This project requires a Google Gemini API key.

Go to Google AI Studio.

Create a new API key.

4. Run the Streamlit App

Launch the Streamlit app from your terminal.

streamlit run streamlit_app.py


Your browser will automatically open to the app.

5. Use the App

Paste your GOOGLE_API_KEY into the sidebar.

Type your high-level goal (e.g., "Write a marketing plan for a new vegan bakery") into the main text box.


Click the "🚀 Run Crew" button and watch the agents work!
