from llama_index.core.tools.tool_spec.base import BaseToolSpec
from app.engine.db import generate_query_engine
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

db_connection_string = os.getenv("DB_CONNECTION_STRING")

class TextToSQLSpec(BaseToolSpec):
    """Text to SQL Spec"""
    
    spec_functions = ["text_to_sql"]
    
    def text_to_sql(self, query:str):
        "A tool for converting natural language to SQL. When user asks a question this tool converts that question to SQL."
        
        print()
        print("Query:")
        print(query)
        print("------------")
        
        query_engine = generate_query_engine()
        sql = query_engine.query(query)
        sql_query = sql.metadata["sql_query"]
        
        if "DELETE" in sql_query or "UPDATE" in sql_query:
            raise Exception("Invalid query.")
        
        print("SQL:")
        print(sql_query)
        
        engine = create_engine(db_connection_string)
        
        with engine.connect() as con:
            rows = con.execute(text(sql_query))
        
        
        response = rows.all()
        print("Response:")
        print(response)
        print()
        
        return {
            "result": response,
            "instruction": "Interpretate the data based on a given query."
        }
        

