import os

from llama_index.core.llms import MessageRole
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from fastapi.responses import Response
from fastapi import APIRouter, HTTPException, Request, status

from app.classes.chat_data import _ChatData, _DecisionMessage, _DecisionType
from app.engine.agents.holiday_agent.holiday_agent import get_holiday_agent
from app.engine.agents.sql_agent.sql_agent import get_sql_agent
from app.engine.router_prompt import get_router_prompt

model = os.getenv("MODEL")
environment = os.getenv("ENVIRONMENT", "dev")

router_llm = OpenAI()

chat_router = r = APIRouter()

verbose = True


# def build_router_messages(messages, last_user_message, max_history=5):
#     history = [m for m in messages if m.role == MessageRole.USER]
#     history = history[-max_history:]

#     router_msgs = [
#         ChatMessage(role=MessageRole.SYSTEM, content=ROUTER_PROMPT),
#     ]

#     for m in history:
#         router_msgs.append(
#             ChatMessage(role=MessageRole.USER, content=m.content)
#         )

#     router_msgs.append(
#         ChatMessage(role=MessageRole.USER, content=last_user_message)
#     )

#     return router_msgs

# async def route_message_with_context(messages, last_user_text):
#     router_messages = build_router_messages(messages, last_user_text)

#     llm_resp = await router_llm.achat(router_messages)
#     raw = llm_resp.message.content

#     decision = _DecisionMessage.model_validate_json(raw)

#     return decision.message

def get_agent_user_message(data:_ChatData):
    agent_message = ""
    user_message = ""
    for m in data.messages[-2:]:
        if m.role == "user":
            user_message = m.content
        else:
            agent_message = m.content

    return agent_message, user_message

def route_query(agent_message:str, user_message:str):
    prompt = get_router_prompt(agent_message, user_message)
    res = OpenAI().complete(prompt, formatted=True)

    if verbose:
        print("prompt:\n ", prompt)
        print("------------------")
        print("Route to: \n", str(res))
        print("-----------------------------")
    
    raw = res.text
    
    print("Raw response:")
    print(raw)
    
    decision = _DecisionMessage.model_validate_json(raw)
    return decision

@r.post("")
async def chat(
    data: _ChatData
):
    
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided.",
        )
        
        
    agent_message, user_message = get_agent_user_message(data)
        
    lastMessage = data.messages.pop()
    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user.",
        )
        
    messages = [ChatMessage(role=m.role, content=m.content) for m in data.messages]
    
    
     # 1) ROUTE
    decision = route_query(agent_message=agent_message, user_message=user_message)
    print("Router decision:", decision)

    print("prompt: \n", lastMessage)
    print("----------------------------------")

    print("Fetching the agent...")

    # 2) PICK AGENT
    if decision.message == _DecisionType.SQL_AGENT:
        print("Fetcing sql agent...")
        agent = get_sql_agent()
    else:
        print("Fetching holiday agent...")
        agent = get_holiday_agent()
    
    
    print("Running the agent...")
    
    response = await agent.run(lastMessage.content, messages)
    
    print()
    print("response:")
    print(str(response))
    print("----------------------------------")

    return Response(str(response))