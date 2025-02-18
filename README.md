# LangChain:SQL Database Chatbot 
This project is a Streamlit-based chatbot application that allows users to interact with SQL databases using LangChain. It supports both SQLite and MySQL databases and leverages a large language model (LLM) from Groq for natural language processing.

## Features
Chat with an SQL Database: Query data using natural language.
Supports Multiple Databases: Works with SQLite and MySQL.
Streamlit UI: Easy-to-use interface for database interaction.
LangChain Integration: Uses LangChain agents and toolkits for query execution.
LLM Support: Leverages the Llama3-8b-8192 model for intelligent responses.

## Requirements
Ensure you have the following installed:
Python 3.x
Streamlit
LangChain
SQLAlchemy
SQLite3
MySQL Connector (if using MySQL)

## Configuration
SQLite: The default database is student.db.
MySQL: Provide MySQL credentials via the sidebar.

## Usage
Select the database type (SQLite or MySQL) from the sidebar.
If using MySQL, enter the required credentials.
Type your query in the chat input box.
Receive responses from the LLM-powered chatbot.
