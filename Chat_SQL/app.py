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

st.set_page_config(page_title="LangChain :Chat with SQL DB",page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCAlDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["USE SQLITE 3 DATABASE- STUDENT.db","Connect to you SQL Database"] #konsa database use krni hai 

selected_opt=st.sidebar.radio(label="Choose the DB Which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MySQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL password",type="password")
    mysql_db=st.sidebar.text_input("MySQL database")
else:
    db_uri=LOCAlDB

if not db_uri:
    st.info("Please Enter the database information and uri")

#llm model calling
llm=ChatGroq(api_key="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",model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCAlDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        # print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True) #connect and only read the file 
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))   
    
if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_uri)

#now for that chat we need a toolkit 
toolkit=SQLDatabaseToolkit(db=db,llm=llm)
agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):   #when starting their no messages so we this ,sessionsate basically dictonary hai and yeh ap ki state koa maintain rakh they hai 
    st.session_state["messages"]=[
        {"role":"assitant","content":"Hi,I'm a chatbot who can search from the  web .how can i help you"}]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)

        
#now for the sqldatabase you need the following 
#localhost:3306
#
#
# there is some error in this mysqlworkbench zr dekh lao 