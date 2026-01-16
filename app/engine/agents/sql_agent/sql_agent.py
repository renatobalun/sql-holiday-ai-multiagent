import os
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from app.engine.tools.text_to_sql import TextToSQLSpec
from app.engine.agents.sql_agent.prompt import get_system_prompt

load_dotenv()

openai_model = os.getenv("MODEL")
openai_llm = OpenAI(model=openai_model)

def get_sql_agent():
    text_to_sql_tool = TextToSQLSpec().to_tool_list()
    
    tools = (text_to_sql_tool)
    
    agent = FunctionAgent(
        tools=tools,
        llm=openai_llm,
        verbose=True,
        system_prompt=get_system_prompt(),
        max_function_calls=1
    )
    
    return agent