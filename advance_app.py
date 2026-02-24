import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI SQL Analytics Assistant",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📊 AI-Powered SQL Analytics Assistant")
st.markdown("""
This assistant helps **Sales & Partner Managers** generate insights from the database  
without writing SQL queries.

Simply ask your business question below.
""")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Configuration")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = ["Use Local SQLite DB", "Connect to MySQL Database"]
selected_opt = st.sidebar.radio("Choose Database", radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("Database Name")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Please enter your Groq API Key to continue.")
    st.stop()

# ---------------- LLM ----------------
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    streaming=True
)

# ---------------- DATABASE CONFIG ----------------
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))

    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL details.")
            st.stop()

        return SQLDatabase(
            create_engine(
                f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            )
        )

if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

# ---------------- AGENT ----------------
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello 👋 Ask me any business question related to your database."}
    ]

if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat history cleared. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- USER INPUT ----------------
user_query = st.chat_input("Ask your business question here...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data and generating insights..."):
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
