import os
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from app.engine.agents.holiday_agent.prompt import get_system_prompt

load_dotenv()

openai_model = os.getenv("MODEL")
openai_llm = OpenAI(model=openai_model)

def get_holiday_agent():
    
    agent = FunctionAgent(
        llm=openai_llm,
        verbose=True,
        system_prompt=get_system_prompt(),
        max_function_calls=1
    )
    
    return agent