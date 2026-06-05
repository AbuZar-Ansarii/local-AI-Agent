from typing import TypedDict, Annotated, Sequence, Any
from langchain_core.messages import BaseMessage
import operator

# The state object for our LangGraph agent
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_id: int
    context: str
    errors: list[str]
    next_step: str
