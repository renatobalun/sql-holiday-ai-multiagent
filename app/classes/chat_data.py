from enum import Enum
from pydantic import BaseModel
from typing import List
from llama_index.core.llms import MessageRole

SQL_AGENT = "SQL_AGENT"
HOLIDAY_AGENT = "HOLIDAY_AGENT"


class _Message(BaseModel):
    role: MessageRole
    content: str
    
class _ChatData(BaseModel):
    messages: List[_Message]
    
class _DecisionType(str, Enum):
    SQL_AGENT = "SQL_AGENT"
    HOLIDAY_AGENT = "HOLIDAY_AGENT"
    
class _DecisionMessage(BaseModel):
    message: _DecisionType