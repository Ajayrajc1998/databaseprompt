import streamlit as st
from langchain.llms.openai import OpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os
import time  # Added for simulating a delay (remove this in production)

# Load environment variables
load_dotenv()

# Define your OpenAI API key
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Define your PostgreSQL connection details
db_connection_uri = 'postgresql+psycopg2://postgres:password@localhost:5432/aiprompt'

# Create a function to run the backend code
def run_backend(query):
    from langchain.chat_models import ChatOpenAI
       
    # Create an instance of ChatOpenAI
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    # Create an instance of SQLDatabase
    db = SQLDatabase.from_uri(db_connection_uri)

    # Create an instance of SQLDatabaseToolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Create an instance of AgentExecutor
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True, handle_parsing_errors=True)

    # Simulate a delay (remove this in production)
    time.sleep(3)

    # Run your agent with the query
    result = agent_executor.run(query)

    # Return the result
    return result

# Create a Streamlit app
st.title("Resume Score Data Prompt")

# Input box for entering queries
query = st.text_input("Enter your query:")

# Initialize a spinner
with st.spinner("Running analysis..."):
    if st.button("Run"):
        if query:
            result = run_backend(query)
            st.write("O/P:", result)
        else:
            st.warning("Please enter a query.")
