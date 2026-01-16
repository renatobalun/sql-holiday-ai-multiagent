from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import text

load_dotenv()

db_connection_string = os.getenv("DB_CONNECTION_STRING")

def generate_query_engine():
    engine = create_engine(db_connection_string)
    llm = OpenAI(temperature=0.1, model="gpt-4.1-mini")
    sql_database = SQLDatabase(engine=engine)
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, llm=llm, sql_only=True, synthesize_response=False
    )
    
    return query_engine