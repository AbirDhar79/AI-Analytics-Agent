"""
AI-Powered SQL Analytics Assistant.

3-step flow (no agent, no loop):
  1. LLM reads schema  ->  generates SQL
  2. QuerySQLDatabaseTool  ->  runs SQL on real DB
  3. LLM reads result  ->  formats plain-English answer
"""
import re
import sqlite3
from pathlib import Path

import streamlit as st
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from sqlalchemy import create_engine, inspect as sa_inspect, text
from sqlalchemy.engine import URL

MODEL_OPTIONS = {
    "LLaMA 3.1 8B (fast, free)":    "llama-3.1-8b-instant",
    "LLaMA 3.3 70B (most capable)": "llama-3.3-70b-versatile",
    "Mixtral 8x7B (large context)": "mixtral-8x7b-32768",
    "Gemma 2 9B (Google)":          "gemma2-9b-it",
}

DB_OPTIONS = {
    "🎓 Academic — student.db":          "student.db",
    "🛒 Sales & E-commerce — sales.db":  "sales.db",
    "👥 HR & People — hr.db":            "hr.db",
    "🔌 Connect to MySQL":               "MYSQL",
}

SAMPLE_QUESTIONS = {
    "student.db": [
        "List all students with marks above 80",
        "Which department has the highest budget?",
        "Top 3 products by total sales revenue",
        "Show employees hired after 2022",
        "Average salary by department",
        "Products with stock below 50",
    ],
    "sales.db": [
        "Total revenue by product category",
        "Which customer placed the most orders?",
        "Top 5 campaigns by conversion rate",
        "Products with less than 50 units in stock",
        "Monthly revenue trend for 2024",
        "Show all delivered orders in Q1 2024",
    ],
    "hr.db": [
        "Average salary by department",
        "Employees with approved leave this year",
        "Top 5 performers by bonus amount",
        "Which department has the most open job postings?",
        "Show all active employees hired after 2021",
        "List employees currently on leave",
    ],
}


def _clean_sql(raw: str) -> str:
    """Strip prefixes/fences the LLM sometimes wraps around the SQL."""
    cleaned = raw.strip()
    for prefix in ("SQLQuery:", "SQL Query:", "SQL:", "sql:", "sqlquery:"):
        if cleaned.lower().startswith(prefix.lower()):
            cleaned = cleaned[len(prefix):].strip()
    cleaned = re.sub(r"^```(?:sql)?\n?", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def _handle_llm_error(e: Exception) -> dict:
    err = str(e).lower()
    if "401" in err or "authentication" in err or "invalid api key" in err or "api_key" in err:
        msg = (
            "**Invalid API key.** The key you entered was rejected by Groq.\n\n"
            "- Double-check it at [console.groq.com](https://console.groq.com)\n"
            "- Paste a fresh key in the sidebar and try again."
        )
    elif "429" in err or "rate limit" in err or "ratelimit" in err:
        msg = (
            "**Rate limit reached.** Your Groq free-tier key has hit its limit "
            "(30 req/min or 500 req/day).\n\n"
            "- Wait 60 seconds and retry\n"
            "- Switch to a different model in the sidebar\n"
            "- Or get a new key at [console.groq.com](https://console.groq.com)"
        )
    elif "quota" in err or "insufficient_quota" in err or "billing" in err:
        msg = (
            "**Quota exceeded.** This API key has no remaining credits.\n\n"
            "- Get a free key at [console.groq.com](https://console.groq.com)\n"
            "- Paste it in the sidebar."
        )
    elif "model" in err and ("not found" in err or "does not exist" in err or "deprecated" in err):
        msg = (
            "**Model unavailable.** The selected model may be deprecated or temporarily down.\n\n"
            "- Choose a different model from the dropdown in the sidebar."
        )
    elif "connection" in err or "timeout" in err or "network" in err or "service unavailable" in err:
        msg = (
            "**Connection error.** Could not reach the Groq API.\n\n"
            "- Check your internet connection\n"
            "- Try again in a few seconds."
        )
    else:
        msg = (
            f"**Unexpected error:** {e}\n\n"
            "- Try a different model from the sidebar\n"
            "- Check your API key at [console.groq.com](https://console.groq.com)"
        )
    return {"answer": msg, "query": "", "raw_result": "", "error": True}


def _is_sql_error(result: str) -> bool:
    """Return True if the executor returned an error string instead of data."""
    lowered = result.strip().lower()
    return lowered.startswith("error:") or "sqlite3.operationalerror" in lowered


def _generate_sql(llm, dialect: str, schema: str, question: str, prior_error: str = "") -> str:
    """Ask the LLM to generate SQL, optionally with a prior error for self-correction."""
    if prior_error:
        system_msg = (
            f"You are a SQL expert. Your previous query failed with this error:\n"
            f"{prior_error}\n\n"
            f"Fix the query. Study the schema carefully — only use column names that actually "
            f"exist in the tables shown. Use JOINs through intermediate tables where needed.\n"
            f"Return ONLY the corrected raw SQL query — no explanation, no markdown, no code fences.\n\n"
            f"Database schema:\n{schema}"
        )
    else:
        system_msg = (
            f"You are a SQL expert. Generate a syntactically correct {dialect} SQL query "
            f"to answer the question.\n"
            f"Study the schema carefully — only use column names that actually exist in the "
            f"tables shown. Use JOINs through intermediate/junction tables where needed.\n"
            f"Return ONLY the raw SQL query — no explanation, no markdown, no code fences.\n\n"
            f"Database schema:\n{schema}"
        )
    response = llm.invoke([SystemMessage(content=system_msg), HumanMessage(content=question)])
    return _clean_sql(response.content)


def ask_database(question: str, db: SQLDatabase, llm: ChatGroq) -> dict:
    """Generate SQL, execute it (with one self-correction retry), then format the result."""
    schema = db.get_table_info()
    dialect = db.dialect
    executor = QuerySQLDatabaseTool(db=db)

    try:
        # Attempt 1
        query = _generate_sql(llm, dialect, schema, question)
        try:
            raw_result = executor.run(query)
        except Exception as exec_err:
            raw_result = f"Error: {exec_err}"

        # Retry once if execution returned an error string
        if _is_sql_error(raw_result):
            prior_error = raw_result
            query = _generate_sql(llm, dialect, schema, question, prior_error=prior_error)
            try:
                raw_result = executor.run(query)
            except Exception as exec_err:
                raw_result = f"Error: {exec_err}"

        # If still an error after retry, surface it cleanly
        if _is_sql_error(raw_result):
            return {
                "answer": (
                    f"I was unable to produce a working SQL query after two attempts.\n\n"
                    f"**Last error:** {raw_result}\n\n"
                    f"Try rephrasing your question, or check the Schema Browser in the sidebar "
                    f"to see the available tables and columns."
                ),
                "query": query,
                "raw_result": "",
                "error": True,
            }

        answer_response = llm.invoke([
            SystemMessage(content="You are a helpful data assistant."),
            HumanMessage(content=(
                f"Question: {question}\n"
                f"SQL Query: {query}\n"
                f"SQL Result: {raw_result}\n\n"
                f"Answer the question clearly in plain English."
            )),
        ])
        return {"answer": answer_response.content, "query": query, "raw_result": raw_result}

    except Exception as e:
        return _handle_llm_error(e)


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI SQL Analytics Assistant",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stChatMessage { border-radius: 10px; padding: 10px; }
    .sample-btn > button {
        border-radius: 20px;
        font-size: 0.82rem;
        padding: 0.3rem 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 AI-Powered SQL Analytics Assistant")
st.markdown(
    "Chat with any of the demo databases below, or connect your own MySQL.  \n"
    "Just ask a question in plain English — no SQL needed."
)

# ── Sidebar ── Configuration ──────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuration")

selected_db_label = st.sidebar.radio("Choose Database", list(DB_OPTIONS.keys()))
selected_dbfile = DB_OPTIONS[selected_db_label]
is_mysql = selected_dbfile == "MYSQL"

mysql_host = mysql_user = mysql_password = mysql_db = mysql_port = None
if is_mysql:
    mysql_host     = st.sidebar.text_input("MySQL Host")
    mysql_user     = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db       = st.sidebar.text_input("Database Name")
    mysql_port     = st.sidebar.text_input("MySQL Port", value="3306", placeholder="3306")

# API key
api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="gsk_…",
    help="Get your free key at console.groq.com",
)

_placeholder_patterns = ("your_", "gsk_xxx", "xxxxxxx", "_here", "example")
_key_looks_valid = (
    bool(api_key)
    and len(api_key) > 20
    and not any(p in api_key.lower() for p in _placeholder_patterns)
)

if _key_looks_valid:
    st.sidebar.success("✅ API key looks valid")
else:
    st.sidebar.warning("⚠️ Enter your Groq API key above")

st.sidebar.markdown(
    "ℹ️ **Free tier:** ~30 req/min, 500 req/day per key.  \n"
    "[Get a free key →](https://console.groq.com)"
)

# Model picker
selected_model_label = st.sidebar.selectbox("LLM Model", list(MODEL_OPTIONS.keys()))
model_name = MODEL_OPTIONS[selected_model_label]

# ── Guards ────────────────────────────────────────────────────────────────────
if not _key_looks_valid:
    st.info(
        "Please add your Groq API key in the sidebar to continue.  \n"
        "Get a free key at [console.groq.com](https://console.groq.com)."
    )
    st.stop()

if is_mysql and not (mysql_host and mysql_user and mysql_password and mysql_db):
    st.error("Please provide all MySQL connection details (Host, User, Password, Database).")
    st.stop()

# ── Database ──────────────────────────────────────────────────────────────────
@st.cache_resource(ttl="2h")
def configure_db(dbfile, host=None, user=None, password=None, database=None, port=None):
    if dbfile != "MYSQL":
        dbfilepath = (Path(__file__).parent / dbfile).absolute()
        if not dbfilepath.exists():
            raise FileNotFoundError(
                f"{dbfile} not found. Run `python create_{dbfile.replace('.db', '_db.py')}` first."
            )
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))

    port = int(port or "3306")
    url = URL.create(
        drivername="mysql+mysqlconnector",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )
    engine = create_engine(url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return SQLDatabase(engine)


try:
    if is_mysql:
        db = configure_db("MYSQL", mysql_host, mysql_user, mysql_password, mysql_db, mysql_port)
    else:
        db = configure_db(selected_dbfile)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(f"Cannot connect to database: {e}")
    st.stop()

llm = ChatGroq(groq_api_key=api_key, model_name=model_name, streaming=False)

# ── Sidebar ── Schema browser ─────────────────────────────────────────────────
with st.sidebar.expander("📋 Schema Browser"):
    try:
        inspector = sa_inspect(db._engine)
        for tbl in inspector.get_table_names():
            st.markdown(f"**{tbl}**")
            for col in inspector.get_columns(tbl):
                st.markdown(
                    f"&nbsp;&nbsp;&nbsp;`{col['name']}` *{col['type']}*",
                    unsafe_allow_html=True,
                )
    except Exception:
        st.code(db.get_table_info())

# ── Sidebar ── How it works ───────────────────────────────────────────────────
with st.sidebar.expander("💡 How it works"):
    st.markdown("""
**NL2SQL — how it relates to RAG**

In RAG the LLM receives retrieved document chunks as context.
Here the "retrieval" is deterministic — the database schema is injected as structured context.

1. **Schema → SQL** — LLM reads your schema and writes a SQL query
2. **SQL → Result** — Query runs on the real database
3. **Result → Answer** — LLM formats the raw result into plain English

No vector store needed: the schema IS the knowledge base.
""")

# ── Sidebar ── Public deployment note ────────────────────────────────────────
with st.sidebar.expander("🌐 Public deployment"):
    st.info(
        "Each visitor uses their **own Groq key** → their own rate limits.  \n"
        "Safe to deploy on **Streamlit Cloud** and **Hugging Face Spaces**."
    )

# ── Sidebar ── Clear history ──────────────────────────────────────────────────
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat history cleared. How can I help you?", "query": ""}
    ]
    st.rerun()

# ── Sample questions (per database) ──────────────────────────────────────────
active_questions = SAMPLE_QUESTIONS.get(selected_dbfile, [])
if active_questions:
    st.markdown("**Try a sample question:**")

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

if active_questions:
    sq_cols = st.columns(3)
    for i, q in enumerate(active_questions):
        if sq_cols[i % 3].button(q, key=f"sq_{selected_dbfile}_{i}", use_container_width=True):
            st.session_state.pending_question = q

# ── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello 👋 Ask me any question about the database.",
            "query": "",
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("error"):
            st.warning(msg["content"])
        else:
            st.markdown(msg["content"])
        if msg.get("query"):
            with st.expander("View generated SQL"):
                st.code(msg["query"], language="sql")

# ── User input ────────────────────────────────────────────────────────────────
user_query = st.chat_input("Ask your question here...")

if not user_query and st.session_state.pending_question:
    user_query = st.session_state.pending_question
    st.session_state.pending_question = ""

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query, "query": ""})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data and generating insights..."):
            result = ask_database(user_query, db, llm)

        if result.get("error"):
            st.warning(result["answer"])
        else:
            st.markdown(result["answer"])
            if result.get("query"):
                with st.expander("View generated SQL"):
                    st.code(result["query"], language="sql")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "query": result.get("query", ""),
        "error": result.get("error", False),
    })
